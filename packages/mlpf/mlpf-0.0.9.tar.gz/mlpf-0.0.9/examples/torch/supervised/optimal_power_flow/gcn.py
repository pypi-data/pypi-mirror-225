import torch

import torch.nn as nn
import torch_geometric as pyg

from sklearn.model_selection import train_test_split
from torch_geometric.loader import DataLoader
from torchmetrics import MetricCollection, MeanSquaredError, R2Score
from tqdm import tqdm

from mlpf.data.data.optimal_power_flow import OptimalPowerFlowData
from mlpf.data.loading.load_data import load_data
from mlpf.loss.torch.metrics.active import MeanActivePowerError, MeanRelativeActivePowerError
from mlpf.loss.torch.metrics.bounds.active import MeanUpperActivePowerError, MeanLowerActivePowerError
from mlpf.loss.torch.metrics.bounds.reactive import MeanUpperReactivePowerError, MeanLowerReactivePowerError
from mlpf.loss.torch.metrics.bounds.voltage import MeanUpperVoltageError, MeanLowerVoltageError
from mlpf.loss.torch.metrics.costs import MeanActivePowerCost, MeanRelativeActivePowerCost
from mlpf.loss.torch.metrics.reactive import MeanReactivePowerError, MeanRelativeReactivePowerError
from mlpf.utils.progress_bar import CustomProgressBar
from mlpf.utils.standard_scaler import StandardScaler


class GNN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, num_layers, out_channels, standard_scaler):
        super(GNN, self).__init__()
        self.standard_scaler = standard_scaler
        self.graph_encoder = pyg.nn.GCN(in_channels=in_channels, hidden_channels=hidden_channels, num_layers=num_layers, out_channels=hidden_channels)
        self.linear = nn.Linear(in_features=hidden_channels, out_features=out_channels)

    def forward(self, data):
        out = self.standard_scaler(data.x)
        out = self.graph_encoder(x=out, edge_index=data.edge_index)
        out = self.linear(out)[~data.PQVA_mask].reshape(data.target_vector.shape)

        return out


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Random seeds
    pyg.seed_everything(123)

    # Hyperparameters
    num_epochs = 1000
    batch_size = 512
    hidden_channels = 100
    num_layers = 3
    learning_rate = 3e-4

    # Generate ppcs

    solved_ppc_list = load_data("solved_opf_ppcs_case118_10k", max_samples=2000)

    opf_data = [OptimalPowerFlowData(solved_ppc).to_pyg_data() for solved_ppc in tqdm(solved_ppc_list, desc="Converting ppcs to data")]

    for data in opf_data:
        data.x[~data.PQVA_mask] = 0.0  # delete the target info from the input features

    data_train, data_val = train_test_split(opf_data, test_size=0.33, random_state=42)

    # Torch dataloaders

    train_loader = DataLoader(data_train, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(data_val, batch_size=batch_size, shuffle=False)

    node_features_stacked = torch.vstack([data.x for data in data_train])
    train_targets = torch.vstack([data.target_vector for data in data_train])

    output_size = train_targets.shape[1]

    output_scaler = StandardScaler(train_targets)
    output_scaler.to(device)

    # Model

    standard_scaler = StandardScaler(node_features_stacked)
    model = GNN(in_channels=node_features_stacked.shape[1],
                hidden_channels=hidden_channels,
                num_layers=num_layers,
                out_channels=data_train[0].PQVA_matrix.shape[1],
                standard_scaler=standard_scaler)
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    criterion = nn.MSELoss()

    # Metrics

    metrics_train = MetricCollection(
        MeanSquaredError(),
        R2Score(num_outputs=output_size),
        MeanActivePowerError(),
        MeanRelativeActivePowerError(),
        MeanReactivePowerError(),
        MeanRelativeReactivePowerError(),
        MeanActivePowerCost(),
        MeanRelativeActivePowerCost(),
        MeanUpperVoltageError(),
        MeanLowerVoltageError(),
        MeanUpperActivePowerError(),
        MeanLowerActivePowerError(),
        MeanUpperReactivePowerError(),
        MeanLowerReactivePowerError()
    ).to(device)

    metrics_val = MetricCollection(
        MeanSquaredError(),
        R2Score(num_outputs=output_size),
        MeanActivePowerError(),
        MeanRelativeActivePowerError(),
        MeanReactivePowerError(),
        MeanRelativeReactivePowerError(),
        MeanActivePowerCost(),
        MeanRelativeActivePowerCost(),
        MeanUpperVoltageError(),
        MeanLowerVoltageError(),
        MeanUpperActivePowerError(),
        MeanLowerActivePowerError(),
        MeanUpperReactivePowerError(),
        MeanLowerReactivePowerError()
    ).to(device)

    # if running from the IDE console, make sure to select 'emulate terminal' in the run configuration, otherwise the output will look bad
    progress_bar = CustomProgressBar(metrics_train.keys(), total=num_epochs)

    for epoch in range(num_epochs):

        # Training
        model.train()
        for batch in train_loader:
            batch = batch.to(device)

            optimizer.zero_grad()

            predictions = model(batch)
            loss = criterion(predictions, output_scaler(batch.target_vector))
            loss.backward()

            metrics_train(preds=predictions, target=output_scaler(batch.target_vector), power_flow_predictions=output_scaler.inverse(predictions), batch=batch)

            optimizer.step()

        # Validation
        with torch.no_grad():

            model.eval()
            for batch in val_loader:
                batch = batch.to(device)

                predictions = model(batch)

                metrics_val(preds=predictions, target=output_scaler(batch.target_vector), power_flow_predictions=output_scaler.inverse(predictions), batch=batch)

        progress_bar.update(metrics_train, metrics_val)

        metrics_train.reset()
        metrics_val.reset()


if __name__ == '__main__':
    main()
