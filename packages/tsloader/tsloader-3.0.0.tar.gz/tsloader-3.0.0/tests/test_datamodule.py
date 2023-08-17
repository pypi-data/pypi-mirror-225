import datetime
import tempfile

import pytest
import pandas as pd
import numpy as np

from tsloader import TimeSeriesDataset, TimeSeriesDataModule

FORECAST_SIZE = 48
STRIDE_SIZE = 24


@pytest.fixture
def datamodule():
    class DefaultDataset(TimeSeriesDataset):
        columns_inputs = ["in1", "in2", "in3"]
        columns_targets = ["out1", "out2"]
        split = "train"
        forecast_size = FORECAST_SIZE
        stride_size = 24

    class DataModule(TimeSeriesDataModule):
        Dataset = DefaultDataset

    return DataModule


@pytest.fixture
def dataloader(dataframe, datamodule):
    dm = datamodule(dataframe, batch_size=1)
    dm.setup()
    return dm.train_dataloader()


def test_datamodule_from_csv(dataframe, datamodule):
    # Load datamodule from dataframe
    dm = datamodule(dataframe, batch_size=1)
    dm.setup()

    # Load datamodule from csv file
    # First define a dataset with a preprocess function
    class DefaultDataset(TimeSeriesDataset):
        columns_inputs = ["in1", "in2", "in3"]
        columns_targets = ["out1", "out2"]
        split = "train"
        forecast_size = FORECAST_SIZE
        stride_size = 24

        def preprocess(self):
            self.df.index = pd.DatetimeIndex(self.df["datetime"])
            self.df.drop(columns="datetime", inplace=True)

    class DataModule(TimeSeriesDataModule):
        Dataset = DefaultDataset

    # Then write dataframe to csv and load it
    with tempfile.NamedTemporaryFile() as fp:
        dataframe.to_csv(fp.name, index_label="datetime")
        dm_fromcsv = DataModule.from_csv(fp.name, batch_size=1)
    dm_fromcsv.setup()
    # Compare both
    assert (dm.dataset_train.df.columns == dm_fromcsv.dataset_train.df.columns).all()
    assert (dm.dataset_train.df.index == dm_fromcsv.dataset_train.df.index).all()
    assert dm.dataset_train.df.shape == dm_fromcsv.dataset_train.df.shape


def test_dataloader_length(dataloader):
    assert len(dataloader) == 7 - FORECAST_SIZE // 24 + 1


def test_forecast_size(dataloader):
    for command, observation in dataloader:
        assert command.shape[0] == FORECAST_SIZE
        assert observation.shape[0] == FORECAST_SIZE
