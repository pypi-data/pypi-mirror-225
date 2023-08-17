import datetime

import torch
from torch.utils.data import Dataset
import numpy as np
import pandas as pd


class TimeSeriesDataset(Dataset):
    """Abstract pytorch :py:class:`~torch.utils.data.Dataset` for time series.

    This module creates a time series dataset from an input
    :py:class:`~pandas.DataFrame`, wich must include a set of input and target columns,
    along with a :py:class:`~pandas.DatetimeIndex`. Preprocessing of the dataframe can
    be defined in the :py:meth:`preprocess` method. The dataset should be split into
    train, validation and test in the :py:meth:`_flag_split` method, for which a default
    implementation is already defined, based on additional attributes. The following
    attributes must be defined, either in the subclass body or at initialization, see
    the example bellow.

    Attributes
    ----------
    columns_inputs:
        List of input columns from the dataframe.
    columns_targets:
        List of target columns from the dataframe.
    forecast_size:
        Size of the sampled to be returned by the dataset.
    stride_size:
        Number of time steps to skip between two consecutive samples.

    Parameters
    ----------
    df:
        Input dataframe.
    split:
        One of ``"train"``, ``"val"`` or ``"test"``.
    normalization_const:
        Normalization constants used to rescale the input data. If ``None``, these
        constants are inferred from the training split of the data directly by computing
        its mean and variance. Default is ``None``.
    **kwargs:
        Every other named argument are added to the object's attributes.

    Example
    -------
        >>> class Dataset(TimeSeriesDataset):
        ...     columns_inputs = ["foo", "bar"]
        ...     train_start = "2023-03-01"
        >>> Dataset(df, split="train")
        >>> # Or
        >>> class Dataset(TimeSeriesDataset):
        ...     train_start = "2023-03-01"
        >>> Dataset(df, split="train", columns_inputs=["foo", "bar"])
    """

    columns_inputs: list
    columns_targets: list
    forecast_size: int
    stride_size: int
    train_start: datetime.datetime = None
    train_end: datetime.datetime = None
    validation_start: datetime.datetime = None
    validation_end: datetime.datetime = None
    test_start: datetime.datetime = None
    test_end: datetime.datetime = None

    def __init__(
        self,
        df: pd.DataFrame,
        split: str,
        normalization_const: dict = None,
        **kwargs,
    ):
        # Update attributes
        self.df = df.copy()
        self._split = split
        self._normalization_const = normalization_const or {}
        for key, value in kwargs.items():
            self.__setattr__(key, value)
        # Preprocess
        self.preprocess()
        # Define train / val / test splits
        last_date = self.df.index[-1].to_pydatetime()
        self.train_start = self.train_start or self.df.index[0].to_pydatetime()
        self.train_end = self.train_end or last_date
        self.validation_start = self.validation_start or last_date
        self.validation_end = self.validation_end or last_date
        self.test_start = self.test_start or last_date
        self.test_end = self.test_end or last_date
        # Flag splits
        self.df["split"] = self.df.index.map(self._flag_split)
        self.inputs = torch.Tensor(
            self._normalize(
                self.df[self.df.split == split][self.columns_inputs], label="inputs"
            ).values
        )
        self.targets = torch.Tensor(
            self._normalize(
                self.df[self.df.split == split][self.columns_targets], label="targets"
            ).values
        )

    def __getitem__(self, idx):
        current_idx = idx * self.stride_size
        return (
            self.inputs[current_idx : current_idx + self.forecast_size],
            self.targets[current_idx : current_idx + self.forecast_size],
        )

    def __len__(self):
        return (len(self.targets) - self.forecast_size) // self.stride_size + 1

    def preprocess(self):
        """Preprocess the input dataframe.

        This method has access to the input dataframe as ``self.df``. It is responsible
        for defining a :py:class:`~pandas.DatetimeIndex`.
        """
        pass

    def _flag_split(self, date) -> str:
        """Define the split of each sample.

        This function will be mapped to the ``"datetime"`` column in order to create a
        new ``"split"`` column. The default implementation makes use of the following
        attributes of the dataset class.

        Attributes
        ----------
        train_start: :py:class:`datetime.datetime`
            Start of the training split
        train_end: :py:class:`datetime.datetime`
            End of the training split
        validation_start: :py:class:`datetime.datetime`
            Start of the validation split
        validation_end: :py:class:`datetime.datetime`
            End of the validation split
        test_start: :py:class:`datetime.datetime`
            Start of the testing split
        test_end: :py:class:`datetime.datetime`
            End of the testing split

        Returns
        -------
        One of ``"train"``, ``"val"``, ``"test"`` or ``"none"``.
        """
        if self.train_start <= date <= self.train_end:
            return "train"
        elif self.validation_start <= date <= self.validation_end:
            return "val"
        elif self.test_start <= date <= self.test_end:
            return "test"
        else:
            return "none"

    def _normalize(self, df: pd.DataFrame, label: str) -> pd.DataFrame:
        """Normalize a dataframe.

        Compute the mean and standard deviation of the training split of the dataset,
        then for the inputed dataframe substract the mean of each column and divide by
        the standard deviation. These normalization constants are saved for rescaling.

        Parameters
        ----------
        df:
            Variables dataframe.
        label:
            Saving label for mean and std, used for rescaling.

        Returns
        -------
        Normalized dataframe.
        """
        try:
            mean, std = self.normalization_const[label]
        except KeyError:
            mean = self.df[self.df.split == "train"][df.columns].mean().values
            std = self.df[self.df.split == "train"][df.columns].std().values
            self.normalization_const[label] = (mean, std)
        return (df - mean) / std

    def rescale(self, array: np.ndarray, label: str) -> np.ndarray:
        """Rescale a previously normalized array.

        Parameters
        ----------
        array:
            numpy array with shape ``(time, dim)``.
        label:
            label used to normalize the variables.

        Returns
        -------
        Rescaled array.
        """
        try:
            array_mean, array_std = self.normalization_const[label]
        except KeyError:
            raise NameError(f"Can't rescale array with unknown label {label}.")
        return array * array_std + array_mean

    @property
    def normalization_const(self):
        return self._normalization_const
