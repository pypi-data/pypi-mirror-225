import datetime

import pytest

from tsloader import TimeSeriesDataset


@pytest.fixture
def default_dataset_train(dataframe):
    return TimeSeriesDataset(
        dataframe,
        columns_inputs=["in1", "in2", "in3"],
        columns_targets=["out1", "out2"],
        split="train",
        forecast_size=24,
        stride_size=24,
    )


@pytest.fixture
def default_dataset_val(dataframe):
    return TimeSeriesDataset(
        dataframe,
        columns_inputs=["in1", "in2", "in3"],
        columns_targets=["out1", "out2"],
        split="val",
        forecast_size=24,
        stride_size=24,
    )


def test_default_dataset_train_split_size(default_dataset_train):
    assert len(default_dataset_train.targets) == 24 * 7


def test_default_dataset_train_split_length(default_dataset_train):
    assert len(default_dataset_train) == 7


def test_default_dataset_val_split_size(default_dataset_val):
    assert len(default_dataset_val.targets) == 0


def test_dataset_normalization(default_dataset_train):
    assert default_dataset_train.targets.mean() < 1e-6
    assert default_dataset_train.targets.std() < 1.01
    assert default_dataset_train.targets.std() > 0.99


@pytest.fixture
def dataset_train_split(dataframe):
    return TimeSeriesDataset(
        dataframe,
        columns_inputs=["in1", "in2", "in3"],
        columns_targets=["out1", "out2"],
        split="train",
        train_end=datetime.datetime(year=2020, month=1, day=4),
        forecast_size=24,
        stride_size=24,
    )


def test_dataset_train_split_size(dataset_train_split):
    assert len(dataset_train_split.targets) == 24 * 3


def test_dataset_train_split_length(dataset_train_split):
    assert len(dataset_train_split) == 3


@pytest.fixture
def dataset_val_split(dataframe):
    return TimeSeriesDataset(
        dataframe,
        columns_inputs=["in1", "in2", "in3"],
        columns_targets=["out1", "out2"],
        split="val",
        train_end=datetime.datetime(year=2020, month=1, day=4),
        validation_start=datetime.datetime(year=2020, month=1, day=4),
        validation_end=datetime.datetime(year=2021, month=1, day=4),
        forecast_size=24,
        stride_size=24,
    )


def test_dataset_val_split_size(dataset_val_split):
    assert len(dataset_val_split.targets) == 24 * 4


def test_dataset_val_split_length(dataset_val_split):
    assert len(dataset_val_split) == 4
