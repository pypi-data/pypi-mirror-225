import logging

from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import torch

from gretel_synthetics.actgan.base import BaseSynthesizer, random_state
from gretel_synthetics.actgan.column_encodings import (
    BinaryColumnEncoding,
    FloatColumnEncoding,
    OneHotColumnEncoding,
)
from gretel_synthetics.actgan.data_sampler import DataSampler
from gretel_synthetics.actgan.data_transformer import DataTransformer
from gretel_synthetics.actgan.structures import ColumnType, EpochInfo
from gretel_synthetics.actgan.train_data import TrainData
from gretel_synthetics.typing import DFLike
from packaging import version
from torch import optim
from torch.nn import (
    BatchNorm1d,
    Dropout,
    functional,
    LeakyReLU,
    Linear,
    Module,
    ReLU,
    Sequential,
)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# NOTE on data terminology used in ACTGAN: This module operates with 3 different
# representations of the training data (and generated synthetic data).
#
# - original - input data as received in API calls, as DataFrame, same format
#       and style is returned for synthetic samples
# - transformed - compact representation after applying DataTransformer (and
#       usually stored in TrainData instances), columns here are always numeric,
#       but may be in a more compact decoded form than what the actual DNN works
#       on, in particular one-hot or binary encoded columns are stored as
#       integer indices, instead of multiple columns, also known as decoded
# - encoded - representation passed directly to DNNs and should be in proper
#             float32 dtype
#
# During training we apply the transformations from original -> transformed ->
# encoded. And for generation the process reverses, going from encoded
# representation back to the original format.


class Discriminator(Module):
    """Discriminator for the ACTGANSynthesizer."""

    def __init__(self, input_dim, discriminator_dim, pac=10):
        super(Discriminator, self).__init__()
        dim = input_dim * pac
        self.pac = pac
        self.pacdim = dim
        seq = []
        for item in list(discriminator_dim):
            seq += [Linear(dim, item), LeakyReLU(0.2), Dropout(0.5)]
            dim = item

        seq += [Linear(dim, 1)]
        self.seq = Sequential(*seq)

    def calc_gradient_penalty(
        self, real_data, fake_data, device="cpu", pac=10, lambda_=10
    ):
        """Compute the gradient penalty."""
        alpha = torch.rand(real_data.size(0) // pac, 1, 1, device=device)
        alpha = alpha.repeat(1, pac, real_data.size(1))
        alpha = alpha.view(-1, real_data.size(1))

        interpolates = alpha * real_data + ((1 - alpha) * fake_data)

        disc_interpolates = self(interpolates)

        gradients = torch.autograd.grad(
            outputs=disc_interpolates,
            inputs=interpolates,
            grad_outputs=torch.ones(disc_interpolates.size(), device=device),
            create_graph=True,
            retain_graph=True,
            only_inputs=True,
        )[0]

        gradients_view = gradients.view(-1, pac * real_data.size(1)).norm(2, dim=1) - 1
        gradient_penalty = ((gradients_view) ** 2).mean() * lambda_

        return gradient_penalty

    def forward(self, input_):
        """Apply the Discriminator to the `input_`."""
        return self.seq(input_.view(-1, self.pacdim))


class Residual(Module):
    """Residual layer for the ACTGANSynthesizer."""

    def __init__(self, i, o):
        super(Residual, self).__init__()
        self.fc = Linear(i, o)
        self.bn = BatchNorm1d(o)
        self.relu = ReLU()

    def forward(self, input_):
        """Apply the Residual layer to the `input_`."""
        out = self.fc(input_)
        out = self.bn(out)
        out = self.relu(out)
        return torch.cat([out, input_], dim=1)


class Generator(Module):
    """Generator for the ACTGANSynthesizer."""

    def __init__(self, embedding_dim: int, generator_dim: Sequence[int], data_dim: int):
        super(Generator, self).__init__()
        dim = embedding_dim
        seq = []
        for item in list(generator_dim):
            seq += [Residual(dim, item)]
            dim += item
        seq.append(Linear(dim, data_dim))
        self.seq = Sequential(*seq)

    def forward(self, input_):
        """Apply the Generator to the `input_`."""
        data = self.seq(input_)
        return data


def _gumbel_softmax_stabilized(
    logits: torch.Tensor,
    tau: float = 1,
    hard: bool = False,
    eps: float = 1e-10,
    dim: int = -1,
):
    """Deals with the instability of the gumbel_softmax for older versions of torch.
    For more details about the issue:
    https://drive.google.com/file/d/1AA5wPfZ1kquaRtVruCd6BiYZGcDeNxyP/view?usp=sharing
    Args:
        logits […, num_features]:
            Unnormalized log probabilities
        tau:
            Non-negative scalar temperature
        hard (bool):
            If True, the returned samples will be discretized as one-hot vectors,
            but will be differentiated as if it is the soft sample in autograd
        dim (int):
            A dimension along which softmax will be computed. Default: -1.
    Returns:
        Sampled tensor of same shape as logits from the Gumbel-Softmax distribution.
    """
    for i in range(10):
        transformed = functional.gumbel_softmax(
            logits, tau=tau, hard=hard, eps=eps, dim=dim
        )
        if not torch.isnan(transformed).any():
            return transformed
    raise ValueError("gumbel_softmax returning NaN.")


class ACTGANSynthesizer(BaseSynthesizer):
    """Anyway Conditional Table GAN Synthesizer.

    This is the core class of the ACTGAN interface.

    Args:
        embedding_dim:
            Size of the random sample passed to the Generator. Defaults to 128.
        generator_dim:
            Size of the output samples for each one of the Residuals. A Residual Layer
            will be created for each one of the values provided. Defaults to (256, 256).
        discriminator_dim:
            Size of the output samples for each one of the Discriminator Layers. A Linear Layer
            will be created for each one of the values provided. Defaults to (256, 256).
        generator_lr:
            Learning rate for the generator. Defaults to 2e-4.
        generator_decay:
            Generator weight decay for the Adam Optimizer. Defaults to 1e-6.
        discriminator_lr:
            Learning rate for the discriminator. Defaults to 2e-4.
        discriminator_decay:
            Discriminator weight decay for the Adam Optimizer. Defaults to 1e-6.
        batch_size:
            Number of data samples to process in each step.
        discriminator_steps:
            Number of discriminator updates to do for each generator update.
            From the WGAN paper: https://arxiv.org/abs/1701.07875. WGAN paper
            default is 5. Default used is 1 to match original CTGAN implementation.
        binary_encoder_cutoff:
            For any given column, the number of unique values that should exist before
            switching over to binary encoding instead of OHE. This will help reduce
            memory consumption for datasets with a lot of unique values.
        binary_encoder_nan_handler:
            Binary encoding currently may produce errant NaN values during reverse transformation. By default
            these NaN's will be left in place, however if this value is set to "mode" then those NaN's will
            be replaced by a random value that is a known mode for a given column.
        cbn_sample_size:
            Number of rows to sample from each column for identifying clusters for the cluster-based normalizer.
            This only applies to float columns. If set to ``0``, no sampling is done and all values are considered,
            which may be very slow. Defaults to 250_000.
        log_frequency:
            Whether to use log frequency of categorical levels in conditional
            sampling. Defaults to ``True``.
        verbose:
            Whether to have log progress results. Defaults to ``False``.
        epochs:
            Number of training epochs. Defaults to 300.
        epoch_callback:
            If set to a callable, call the function with `EpochInfo` as the arg
        pac:
            Number of samples to group together when applying the discriminator.
            Defaults to 10.
        cuda:
            Whether to attempt to use cuda for GPU computation.
            If this is False or CUDA is not available, CPU will be used.
            Defaults to ``True``.
    """

    def __init__(
        self,
        embedding_dim: int = 128,
        generator_dim: Sequence[int] = (256, 256),
        discriminator_dim: Sequence[int] = (256, 256),
        generator_lr: float = 2e-4,
        generator_decay: float = 1e-6,
        discriminator_lr: float = 2e-4,
        discriminator_decay: float = 1e-6,
        batch_size: int = 500,
        discriminator_steps: int = 1,
        binary_encoder_cutoff: int = 500,
        binary_encoder_nan_handler: Optional[str] = None,
        cbn_sample_size: Optional[int] = 250_000,
        log_frequency: bool = True,
        verbose: bool = False,
        epochs: int = 300,
        epoch_callback: Optional[Callable] = None,
        pac: int = 10,
        cuda: bool = True,
    ):
        if batch_size % 2 != 0:
            raise ValueError("`batch_size` must be divisible by 2")

        if batch_size % pac != 0:
            raise ValueError("`batch_size` must be divisible by `pac` (defaults to 10)")

        self._embedding_dim = embedding_dim
        self._generator_dim = generator_dim
        self._discriminator_dim = discriminator_dim

        self._generator_lr = generator_lr
        self._generator_decay = generator_decay
        self._discriminator_lr = discriminator_lr
        self._discriminator_decay = discriminator_decay

        self._batch_size = batch_size
        self._discriminator_steps = discriminator_steps
        self._binary_encoder_cutoff = binary_encoder_cutoff
        self._binary_encoder_nan_handler = binary_encoder_nan_handler
        self._log_frequency = log_frequency
        self._cbn_sample_size = cbn_sample_size
        self._verbose = verbose
        self._epochs = epochs
        self._epoch_callback = epoch_callback
        self.pac = pac

        if not cuda or not torch.cuda.is_available():
            device = "cpu"
        elif isinstance(cuda, str):
            device = cuda
        else:
            device = "cuda"

        self._device = torch.device(device)

        self._transformer = None
        self._condvec_sampler = None
        self._generator = None

        self._activation_fns: List[
            Tuple[int, int, Callable[[torch.Tensor], torch.Tensor]]
        ] = []
        self._cond_loss_col_ranges: List[Tuple[int, int, int, int]] = []

        if self._epoch_callback is not None and not callable(self._epoch_callback):
            raise ValueError("`epoch_callback` must be a callable or `None`")

    _gumbel_softmax = staticmethod(
        functional.gumbel_softmax
        if version.parse(torch.__version__) >= version.parse("1.2.0")
        else _gumbel_softmax_stabilized
    )

    def _make_noise(self) -> torch.Tensor:
        """Create new random noise tensors for a batch.

        Returns:
            Tensor of random noise used as (part of the) input to generator
            network. Shape is [batch_size, embedding_dim].
        """
        # NOTE: speedup may be possible if we can reuse the mean and std tensors
        # here across calls to _make_noise.
        mean = torch.zeros((self._batch_size, self._embedding_dim), device=self._device)
        std = mean + 1.0
        return torch.normal(mean, std)

    def _apply_generator(
        self, fakez: torch.Tensor, fake_cond_vec: Optional[torch.Tensor]
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Apply generator network.

        Args:
            fakez: Random noise (z-vectors), shape is [batch_size,
                embedding_dim]
            fake_cond_vec: Optional conditional vectors to guide generation,
                shape is [batch_size, cond_vec_dim]

        Returns:
            Tuple of direct generator output, and output after applying
            activation functions. Shape of both tensor outputs is [batch_size,
            data_dim]
        """
        if fake_cond_vec is None:
            input = fakez
        else:
            input = torch.cat([fakez, fake_cond_vec], dim=1)

        fake = self._generator(input)
        fakeact = self._apply_activate(fake)
        return fake, fakeact

    def _apply_discriminator(
        self,
        encoded: torch.Tensor,
        cond_vec: Optional[torch.Tensor],
        discriminator: Discriminator,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Apply discriminator network.

        Args:
            encoded: Tensor of data in encoded representation to evaluate.
            cond_vec: Optional conditional vector

        Returns:
            Tuple of full input to the discriminator network and the output.
        """
        if cond_vec is None:
            input = encoded
        else:
            input = torch.cat([encoded, cond_vec], dim=1)
        y = discriminator(input)
        return input, y

    def _apply_activate(self, data):
        """Apply proper activation function to the output of the generator."""
        data_t = [
            activation_fn(data[:, st:ed])
            for st, ed, activation_fn in self._activation_fns
        ]

        return torch.cat(data_t, dim=1)

    def _cond_loss(self, data, c, m):
        """Compute the cross entropy loss on the fixed discrete column."""
        loss = [
            functional.cross_entropy(
                data[:, st:ed],
                torch.argmax(c[:, st_c:ed_c], dim=1),
                reduction="none",
            )
            for st, ed, st_c, ed_c in self._cond_loss_col_ranges
        ]

        loss = torch.stack(loss, dim=1)  # noqa: PD013

        return (loss * m).sum() / data.size()[0]

    def _validate_discrete_columns(
        self, train_data: DFLike, discrete_columns: Sequence[str]
    ) -> None:
        """Check whether ``discrete_columns`` exists in ``train_data``.

        Args:
            train_data: Training Data. It must be a 2-dimensional numpy array or a pandas.DataFrame.
            discrete_columns:
                List of discrete columns to be used to generate the Conditional
                Vector. If ``train_data`` is a Numpy array, this list should
                contain the integer indices of the columns. Otherwise, if it is
                a ``pandas.DataFrame``, this list should contain the column names.
        """
        if isinstance(train_data, pd.DataFrame):
            invalid_columns = set(discrete_columns) - set(train_data.columns)
        elif isinstance(train_data, np.ndarray):
            invalid_columns = []
            for column in discrete_columns:
                if column < 0 or column >= train_data.shape[1]:
                    invalid_columns.append(column)
        else:
            raise TypeError("``train_data`` should be either pd.DataFrame or np.array.")

        if invalid_columns:
            raise ValueError(f"Invalid columns found: {invalid_columns}")

    def _prepare_batch(
        self, data_sampler: DataSampler
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """Select a random subset of training data for one batch.

        Also prepares other required Tensors such as conditional vectors, for
        generator and discriminator training.

        Args:
            data_sampler: DataSampler instance that performs sampling

        Returns:
            Tuple of:
              - torch.Tensor or None, fake conditional vector (part of input to
                generator)
              - torch.Tensor or None, real conditional vector associated with
                the encoded real sample returned
              - torch.Tensor or None, column mask indicating which columns (in
                transformed representation) are set in the fake conditional
                vector
              - torch.Tensor, encoded real sample
        """
        fake_cond_vec, fake_column_mask, col, opt = data_sampler.sample_condvec(
            self._batch_size
        )

        if fake_cond_vec is None:
            real_encoded = data_sampler.sample_data(self._batch_size, None, None)
            real_cond_vec = None
        else:
            fake_cond_vec = torch.from_numpy(fake_cond_vec).to(self._device)
            fake_column_mask = torch.from_numpy(fake_column_mask).to(self._device)

            perm = np.random.permutation(self._batch_size)
            real_encoded = data_sampler.sample_data(
                self._batch_size, col[perm], opt[perm]
            )
            real_cond_vec = fake_cond_vec[perm]

        real_encoded = torch.from_numpy(real_encoded.astype("float32")).to(self._device)

        return (
            fake_cond_vec,
            real_cond_vec,
            fake_column_mask,
            real_encoded,
        )

    @random_state
    def fit(
        self, train_data: DFLike, discrete_columns: Optional[Sequence[str]] = None
    ) -> None:
        transformed_train_data = self._pre_fit_transform(
            train_data, discrete_columns=discrete_columns
        )
        self._actual_fit(transformed_train_data)

    def _pre_fit_transform(
        self, train_data: DFLike, discrete_columns: Optional[Sequence[str]] = None
    ) -> TrainData:
        if discrete_columns is None:
            discrete_columns = ()

        self._validate_discrete_columns(train_data, discrete_columns)

        self._transformer = DataTransformer(
            binary_encoder_cutoff=self._binary_encoder_cutoff,
            binary_encoder_nan_handler=self._binary_encoder_nan_handler,
            cbn_sample_size=self._cbn_sample_size,
            verbose=self._verbose,
        )
        self._transformer.fit(train_data, discrete_columns)

        train_data_dec = self._transformer.transform_decoded(train_data)

        self._activation_fns = []
        self._cond_loss_col_ranges = []

        st = 0
        st_c = 0
        for column_info in train_data_dec.column_infos:
            for enc in column_info.encodings:
                ed = st + enc.encoded_dim
                if isinstance(enc, FloatColumnEncoding):
                    self._activation_fns.append((st, ed, torch.tanh))
                elif isinstance(enc, BinaryColumnEncoding):
                    self._activation_fns.append((st, ed, torch.sigmoid))
                elif isinstance(enc, OneHotColumnEncoding):
                    self._activation_fns.append(
                        (st, ed, lambda data: self._gumbel_softmax(data, tau=0.2))
                    )
                    if column_info.column_type == ColumnType.DISCRETE:
                        ed_c = st_c + enc.encoded_dim
                        self._cond_loss_col_ranges.append((st, ed, st_c, ed_c))
                        st_c = ed_c
                else:
                    raise ValueError(f"Unexpected column encoding {type(enc)}")

                st = ed

        return train_data_dec

    def _actual_fit(self, train_data: TrainData) -> None:
        """Fit the ACTGAN Synthesizer models to the training data.

        Args:
            train_data: training data as a TrainData instance
        """

        epochs = self._epochs

        data_sampler = DataSampler(
            train_data,
            self._log_frequency,
        )
        self._condvec_sampler = data_sampler.condvec_sampler

        data_dim = train_data.encoded_dim

        self._generator = Generator(
            self._embedding_dim + data_sampler.cond_vec_dim,
            self._generator_dim,
            data_dim,
        ).to(self._device)

        discriminator = Discriminator(
            data_dim + data_sampler.cond_vec_dim,
            self._discriminator_dim,
            pac=self.pac,
        ).to(self._device)

        optimizerG = optim.Adam(
            self._generator.parameters(),
            lr=self._generator_lr,
            betas=(0.5, 0.9),
            weight_decay=self._generator_decay,
        )

        optimizerD = optim.Adam(
            discriminator.parameters(),
            lr=self._discriminator_lr,
            betas=(0.5, 0.9),
            weight_decay=self._discriminator_decay,
        )

        steps_per_epoch = max(len(train_data) // self._batch_size, 1)
        for i in range(epochs):
            for _ in range(steps_per_epoch):
                for _ in range(self._discriminator_steps):
                    # Optimize discriminator
                    fakez = self._make_noise()
                    (
                        fake_cond_vec,
                        real_cond_vec,
                        fake_column_mask,
                        real_encoded,
                    ) = self._prepare_batch(data_sampler)

                    fake, fakeact = self._apply_generator(fakez, fake_cond_vec)

                    fake_cat, y_fake = self._apply_discriminator(
                        fakeact, fake_cond_vec, discriminator
                    )
                    real_cat, y_real = self._apply_discriminator(
                        real_encoded, real_cond_vec, discriminator
                    )

                    pen = discriminator.calc_gradient_penalty(
                        real_cat, fake_cat, self._device, self.pac
                    )
                    loss_d = -(torch.mean(y_real) - torch.mean(y_fake))

                    optimizerD.zero_grad()
                    pen.backward(retain_graph=True)
                    loss_d.backward()
                    optimizerD.step()

                # Optimize generator
                fakez = self._make_noise()
                (
                    fake_cond_vec,
                    real_cond_vec,
                    fake_column_mask,
                    # Real data is unused here, possible speedup if we skip
                    # creating this Tensor for CTGAN style conditional vectors
                    _,
                ) = self._prepare_batch(data_sampler)

                fake, fakeact = self._apply_generator(fakez, fake_cond_vec)
                fake_cat, y_fake = self._apply_discriminator(
                    fakeact, fake_cond_vec, discriminator
                )

                if fake_cond_vec is None:
                    loss_reconstruction = 0.0
                else:
                    loss_reconstruction = self._cond_loss(
                        fake, fake_cond_vec, fake_column_mask
                    )

                loss_g = -torch.mean(y_fake) + loss_reconstruction

                optimizerG.zero_grad()
                loss_g.backward()
                optimizerG.step()

            _epoch = i + 1
            _loss_g = round(float(loss_g.detach().cpu()), 4)
            _loss_d = round(float(loss_d.detach().cpu()), 4)

            if self._verbose:
                logger.info(
                    f"Epoch: {_epoch}, Loss G: {_loss_g: .4f}, "  # noqa: T001
                    f"Loss D: {_loss_d: .4f}",
                )

            if self._epoch_callback is not None:
                self._epoch_callback(EpochInfo(_epoch, _loss_g, _loss_d))

    @random_state
    def sample(
        self,
        n: int,
        condition_column: Optional[str] = None,
        condition_value: Optional[str] = None,
    ) -> pd.DataFrame:
        """Sample data similar to the training data.

        Choosing a condition_column and condition_value will increase the probability of the
        discrete condition_value happening in the condition_column.

        Args:
            n: Number of rows to sample.
            condition_column: Name of a discrete column.
            condition_value: Name of the category in the condition_column which we wish to increase the
                probability of happening.

        Returns:
            numpy.ndarray or pandas.DataFrame
        """
        if condition_column is not None and condition_value is not None:
            condition_info = self._transformer.convert_column_name_value_to_id(
                condition_column, condition_value
            )
            global_condition_vec = (
                self._condvec_sampler.generate_cond_from_condition_column_info(
                    condition_info, self._batch_size
                )
            )
        else:
            global_condition_vec = None

        # Switch generator to eval mode for inference
        self._generator.eval()
        steps = (n - 1) // self._batch_size + 1
        data = []
        for _ in range(steps):
            if global_condition_vec is not None:
                condvec_numpy = global_condition_vec.copy()
            else:
                condvec_numpy = self._condvec_sampler.sample_original_condvec(
                    self._batch_size
                )

            fakez = self._make_noise()

            if condvec_numpy is not None:
                condvec = torch.from_numpy(condvec_numpy).to(self._device)
            else:
                condvec = None

            fake, fakeact = self._apply_generator(fakez, condvec)

            data.append(fakeact.detach().cpu().numpy())

        # Switch generator back to train mode now that inference is complete
        self._generator.train()
        data = np.concatenate(data, axis=0)
        data = data[:n]

        original_repr_data = self._transformer.inverse_transform(data)
        return original_repr_data

    def set_device(self, device: str) -> None:
        """Set the `device` to be used ('GPU' or 'CPU)."""
        self._device = device
        if self._generator is not None:
            self._generator.to(self._device)
