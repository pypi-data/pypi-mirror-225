from pathlib import Path
import tempfile
from typing import Optional
from typing_extensions import Self

import pandas as pd
import lightning as L
import torch
from torch.utils.data import DataLoader

from .dataset import TimeSeriesDataset


class TimeSeriesDataModule(L.LightningDataModule):
    """Abstract lightning DataModule for time series.

    Attributes
    ----------
    Dataset: :py:class:`~tsloader.dataset.TimeSeriesDataset`
        Time series dataset.

    Parameters
    ----------
    df:
        Input DataFrame.
    batch_size:
        Batch size for torch's :py:class:`~torch.utils.data.DataLoader`.
    num_workers:
        Number of workers for torch's :py:class:`~torch.utils.data.DataLoader`. Default
        is ``2``.
    drop_last:
        If ``True``, will drop last sample of the dataset. Default is ``False``.
    **dataset_kwargs:
        Any further named arguments are fed to the
        :py:class:`~tsloader.dataset.TimeSeriesDataset` class.
    """

    Dataset: TimeSeriesDataset

    def __init__(
        self,
        df: pd.DataFrame,
        batch_size: int,
        num_workers: int = 2,
        drop_last: bool = False,
        **dataset_kwargs
    ):
        super().__init__()
        self.df = df
        self._batch_size = batch_size
        self._num_workers = num_workers
        self._drop_last = drop_last
        self._dataset_kwargs = dataset_kwargs

    def setup(self, stage: Optional[str] = None):
        self.dataset_train = self.Dataset(
            self.df, split="train", **self._dataset_kwargs
        )
        self.dataset_val = self.Dataset(self.df, split="val", **self._dataset_kwargs)
        self.dataset_test = self.Dataset(self.df, split="test", **self._dataset_kwargs)

    def train_dataloader(self, shuffle=True):
        return DataLoader(
            self.dataset_train,
            batch_size=self._batch_size,
            num_workers=self._num_workers,
            shuffle=shuffle,
            drop_last=self._drop_last,
            collate_fn=self._collate_fn,
        )

    def val_dataloader(self):
        return DataLoader(
            self.dataset_val,
            batch_size=self._batch_size,
            num_workers=self._num_workers,
            shuffle=False,
            drop_last=self._drop_last,
            collate_fn=self._collate_fn,
        )

    def test_dataloader(self):
        return DataLoader(
            self.dataset_test,
            batch_size=self._batch_size,
            num_workers=self._num_workers,
            shuffle=False,
            drop_last=self._drop_last,
            collate_fn=self._collate_fn,
        )

    def rescale(self, *args, **kwargs):
        return self.dataset_val.rescale(*args, **kwargs)

    @staticmethod
    def _collate_fn(batch):
        u, y = list(zip(*batch))
        u = torch.stack(u).transpose(0, 1)
        y = torch.stack(y).transpose(0, 1)
        return u, y

    def visualize(self):
        inputs = self.Dataset.columns_inputs
        outputs = self.Dataset.columns_targets
        self.df["split_num"] = self.df["split"].apply(
            lambda split: {
                "train": 1,
                "val": 2,
                "test": 3,
                "none": 0,
            }[split]
        )
        self.df[[*inputs, *outputs, "split_num"]].plot(
            subplots=True,
            include_bool=True,
            figsize=(25, 3 * (len(inputs) + len(outputs))),
        )

    @classmethod
    def from_csv(cls, dataset_path: Path, *args, **kwargs) -> Self:
        """Instantiate a datamodule from csv file.

        Parameters
        ==========
        dataset_path:
            Path to the dataset as a csv file.

        Returns
        =======
        An instance of TimeSeriesDataModule
        """
        return cls(df=pd.read_csv(dataset_path), *args, **kwargs)
