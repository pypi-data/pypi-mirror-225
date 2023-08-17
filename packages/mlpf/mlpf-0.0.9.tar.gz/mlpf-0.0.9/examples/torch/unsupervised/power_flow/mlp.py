import torch

import pandapower as pp
import pandapower.networks as pn
import torch.nn as nn
import torch_geometric as pyg

from pypower.ppoption import ppoption
from pypower.runpf import runpf
from sklearn.model_selection import train_test_split
from torch_geometric.loader import DataLoader
from torchmetrics import MetricCollection
from tqdm import tqdm

from mlpf.data.data.power_flow import PowerFlowData
from mlpf.data.generate.generate_uniform_data import generate_uniform_ppcs
from mlpf.loss.torch.metrics.active import MeanActivePowerError, MeanRelativeActivePowerError
from mlpf.loss.torch.metrics.reactive import MeanReactivePowerError, MeanRelativeReactivePowerError
from mlpf.utils.progress_bar import CustomProgressBar
from mlpf.utils.standard_scaler import StandardScaler


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Random seeds
    pyg.seed_everything(123)

    # Hyperparameters
    num_epochs = 1000
    batch_size = 512
    learning_rate = 3e-4

    # Generate ppcs

    net = pn.case118()
    ppc = pp.converter.to_ppc(net, init="flat")

    base_ppc, converged = runpf(ppc, ppopt=ppoption(OUT_ALL=0, VERBOSE=0))

    solved_ppc_list = generate_uniform_ppcs(
        base_ppc,
        how_many=1000,
        low=0.9,
        high=1.1
    )

    pf_data = [PowerFlowData(solved_ppc).to_pyg_data() for solved_ppc in tqdm(solved_ppc_list, desc="Converting ppcs to data")]

    data_train, data_val = train_test_split(pf_data, test_size=0.33, random_state=42)

    # Torch dataloaders

    train_loader = DataLoader(data_train, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(data_val, batch_size=batch_size, shuffle=False)

    input_size = data_train[0].feature_vector.shape[1]
    output_size = data_train[0].target_vector.shape[1]

    train_features = torch.vstack([data.feature_vector for data in data_train])

    # Model
    model = nn.Sequential(
        StandardScaler(train_features),
        nn.Linear(in_features=input_size, out_features=output_size)
    )
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Metrics

    metrics_train = MetricCollection(
        MeanActivePowerError(),
        MeanRelativeActivePowerError(),
        MeanReactivePowerError(),
        MeanRelativeReactivePowerError()
    ).to(device)

    metrics_val = MetricCollection(
        MeanActivePowerError(),
        MeanRelativeActivePowerError(),
        MeanReactivePowerError(),
        MeanRelativeReactivePowerError()
    ).to(device)

    # if running from the IDE console, make sure to select 'emulate terminal' in the run configuration, otherwise the output will look bad
    progress_bar = CustomProgressBar(metrics_train.keys(), total=num_epochs)

    for epoch in range(num_epochs):

        # Training
        model.train()
        for batch in train_loader:
            batch = batch.to(device)

            optimizer.zero_grad()

            predictions = model(batch.feature_vector)
            batch_metrics = metrics_train(power_flow_predictions=predictions, batch=batch)

            loss = batch_metrics['MeanActivePowerError'] + batch_metrics['MeanReactivePowerError']
            loss.backward()

            optimizer.step()

        # Validation
        with torch.no_grad():

            model.eval()
            for batch in val_loader:
                batch = batch.to(device)

                predictions = model(batch.feature_vector)

                metrics_val(power_flow_predictions=predictions, batch=batch)

        progress_bar.update(metrics_train, metrics_val)

        metrics_train.reset()
        metrics_val.reset()


if __name__ == '__main__':
    main()
