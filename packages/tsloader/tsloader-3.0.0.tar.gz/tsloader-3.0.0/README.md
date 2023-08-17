# Time Series Loader

Manage time series dataset to be served as torch dataloaders. The main features are:
 - Load a csv file into dataloaders
 - Handle train/val/test splits
 - Normalize and rescale each variable

## Example usage
We first build a PyTorch Dataset, then a pytorch-lightning DataModule.

```python
from tsloader import TimeSeriesDataset, TimeSeriesDataModule

class ETDataset(TimeSeriesDataset):
    columns_inputs = ["HUFL", "HULL", "MUFL", "MULL", "LUFL", "LULL"]
    columns_targets = ["OT"]

    train_start = datetime.datetime(year=2016, month=7, day=1)
    train_end = validation_start = datetime.datetime(year=2017, month=7, day=1)
    validation_end = test_start = validation_start + datetime.timedelta(days=28 * 4)
    test_end = test_start + datetime.timedelta(days=28 * 4)
    stride_size = 24

    def preprocess(self):
        self.df["datetime"] = self.df["date"].apply(pd.to_datetime)


class ETDataModule(TimeSeriesDataModule):
    Dataset = ETDataset


# Setup the datamodule
datamodule = ETDataModule(
    dataset_path="datasets/ett/ETTh1.csv", forecast_size=48, batch_size=4
)
datamodule.setup()
# Visualize the entire dataset
datamodule.visualize()
# Load a sample from the training dataloader
dataloader = datamodule.train_dataloader()
for commands, observations in dataloader:
    ...
```

## Installation
Using pip, we can simply install the latest release. The main branch is considered stable.
```bash
$ pip install git+https://git.zagouri.org/max/tsloader
```

If you are from Accenta, then you probably want to install the Accenta-specific version of this package:
```bash
$ pip install git+https://git.zagouri.org/max-accenta/tsloader
```

### Compiling the documentation
The required libraries for compiling the documentation are listed in `docs/requirements.txt`. Once installed, run the following command from the `docs/` folder:
```bash
$ make html
```
The documentation is built to the folder `docs/_build/html/`, and can be viewed by moving inside the directory and launching a temporary http server (for instance `python -m http.server`).
