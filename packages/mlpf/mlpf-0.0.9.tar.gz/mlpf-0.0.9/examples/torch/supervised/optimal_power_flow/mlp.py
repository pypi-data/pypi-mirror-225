import copy
import torch

import torch.nn as nn
import torch_geometric as pyg

from sklearn.model_selection import train_test_split
from torch_geometric.loader import DataLoader
from torchmetrics import MetricCollection, MeanSquaredError, R2Score
from tqdm import tqdm

from mlpf.data.data.optimal_power_flow import OptimalPowerFlowData
from mlpf.data.loading.load_data import load_data
from mlpf.loss.torch.metrics.active import (
    MeanActivePowerError,
    MeanRelativeActivePowerError,
    MaxActivePowerError,
    MaxRelativeActivePowerError
)
from mlpf.loss.torch.metrics.bounds.active import (
    MeanLowerActivePowerError,
    MeanUpperActivePowerError,
    MaxUpperActivePowerError,
    MinLowerActivePowerError
)
from mlpf.loss.torch.metrics.bounds.reactive import (
    MeanUpperReactivePowerError,
    MeanLowerReactivePowerError,
    MaxUpperReactivePowerError,
    MinLowerReactivePowerError
)
from mlpf.loss.torch.metrics.bounds.voltage import (
    MeanUpperVoltageError,
    MeanLowerVoltageError,
    MaxUpperVoltageError,
    MinLowerVoltageError
)
from mlpf.loss.torch.metrics.costs import (
    MeanActivePowerCost,
    MeanRelativeActivePowerCost,
    MaxActivePowerCost,
    MaxRelativeActivePowerCost
)
from mlpf.loss.torch.metrics.reactive import (
    MeanReactivePowerError,
    MeanRelativeReactivePowerError,
    MaxReactivePowerError,
    MaxRelativeReactivePowerError
)
from mlpf.utils.progress_bar import CustomProgressBar
from mlpf.utils.standard_scaler import StandardScaler


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Random seeds
    pyg.seed_everything(123)

    # Hyperparameters
    num_epochs = 1000
    batch_size = 1024
    learning_rate = 3e-3

    solved_ppc_list = load_data("solved_opf_ppcs_case118_10k", max_samples=2000)

    opf_data = [OptimalPowerFlowData(solved_ppc).to_pyg_data() for solved_ppc in tqdm(solved_ppc_list, desc="Converting ppcs to data")]

    data_train, data_val = train_test_split(opf_data, test_size=0.33, random_state=42)

    # Torch dataloaders

    train_loader = DataLoader(data_train, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(data_val, batch_size=batch_size, shuffle=False)

    input_size = data_train[0].feature_vector.shape[1]
    output_size = data_train[0].target_vector.shape[1]

    train_features = torch.vstack([data.feature_vector for data in data_train])
    train_targets = torch.vstack([data.target_vector for data in data_train])

    output_scaler = StandardScaler(train_targets)
    output_scaler.to(device)

    # Model
    model = nn.Sequential(
        StandardScaler(train_features),
        nn.Linear(in_features=input_size, out_features=output_size),
    )
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    # Metrics

    metrics_train = MetricCollection(
        MeanSquaredError(),
        R2Score(num_outputs=output_size),

        MeanActivePowerError(),
        MeanRelativeActivePowerError(),
        MaxActivePowerError(),
        MaxRelativeActivePowerError(),

        MeanReactivePowerError(),
        MeanRelativeReactivePowerError(),
        MaxReactivePowerError(),
        MaxRelativeReactivePowerError(),

        MeanActivePowerCost(),
        MeanRelativeActivePowerCost(),
        MaxActivePowerCost(),
        MaxRelativeActivePowerCost(),

        MeanUpperVoltageError(),
        MeanLowerVoltageError(),
        MaxUpperVoltageError(),
        MinLowerVoltageError(),

        MeanUpperActivePowerError(),
        MaxUpperActivePowerError(),
        MeanLowerActivePowerError(),
        MinLowerActivePowerError(),

        MeanUpperReactivePowerError(),
        MeanLowerReactivePowerError(),
        MaxUpperReactivePowerError(),
        MinLowerReactivePowerError()
    ).to(device)

    metrics_val = copy.deepcopy(metrics_train).to(device)

    # if running from the IDE console, make sure to select 'emulate terminal' in the run configuration, otherwise the output will look bad
    progress_bar = CustomProgressBar(metrics_train.keys(), total=num_epochs)

    for epoch in range(num_epochs):

        # Training
        model.train()
        for batch in train_loader:
            batch = batch.to(device)
            features, targets = batch.feature_vector, batch.target_vector

            optimizer.zero_grad()

            predictions = model(features)
            loss = criterion(predictions, output_scaler(targets))
            loss.backward()

            metrics_train(preds=predictions, target=output_scaler(targets), power_flow_predictions=output_scaler.inverse(predictions), batch=batch)

            optimizer.step()

        # Validation
        with torch.no_grad():

            model.eval()
            for batch in val_loader:
                batch = batch.to(device)
                features, targets = batch.feature_vector, batch.target_vector

                predictions = model(features)

                metrics_val(preds=predictions, target=output_scaler(targets), power_flow_predictions=output_scaler.inverse(predictions), batch=batch)

        progress_bar.update(metrics_train, metrics_val)

        metrics_train.reset()
        metrics_val.reset()


if __name__ == '__main__':
    main()
