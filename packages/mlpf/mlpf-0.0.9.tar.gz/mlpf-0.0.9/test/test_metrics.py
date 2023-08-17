import unittest
from typing import Dict, List

import numpy as np
import pandapower as pp
import pandapower.networks as pn
import torch
from pandas import DataFrame

from pypower.ppoption import ppoption
from pypower.runpf import runpf
from torch_geometric.loader import DataLoader
from torchmetrics import MetricCollection
from tqdm import tqdm

from mlpf.data.data.optimal_power_flow import OptimalPowerFlowData
from mlpf.data.data.power_flow import PowerFlowData
from mlpf.data.generate.generate_uniform_data import generate_uniform_ppcs
from mlpf.loss.numpy.metrics.active import ActivePowerError, RelativeActivePowerError
from mlpf.loss.numpy.metrics.bounds.active import UpperActivePowerError, LowerActivePowerError
from mlpf.loss.numpy.metrics.bounds.reactive import UpperReactivePowerError, LowerReactivePowerError
from mlpf.loss.numpy.metrics.bounds.voltage import UpperVoltageError, LowerVoltageError
from mlpf.loss.numpy.metrics.costs import ActivePowerCost, RelativeActivePowerCost
from mlpf.loss.numpy.metrics.metrics import MultipleMetrics
from mlpf.loss.numpy.metrics.reactive import ReactivePowerError, RelativeReactivePowerError
from mlpf.loss.torch.metrics.active import (
    MeanActivePowerError,
    MeanRelativeActivePowerError,
    MaxActivePowerError,
    MaxRelativeActivePowerError,
    MinActivePowerError,
    MinRelativeActivePowerError
)
from mlpf.loss.torch.metrics.bounds.active import (
    MeanLowerActivePowerError,
    MeanUpperActivePowerError,
    MaxUpperActivePowerError,
    MinUpperActivePowerError,
    MaxLowerActivePowerError,
    MinLowerActivePowerError
)
from mlpf.loss.torch.metrics.bounds.reactive import (
    MeanUpperReactivePowerError,
    MeanLowerReactivePowerError,
    MaxUpperReactivePowerError,
    MinUpperReactivePowerError,
    MinLowerReactivePowerError,
    MaxLowerReactivePowerError
)
from mlpf.loss.torch.metrics.bounds.voltage import (
    MeanUpperVoltageError,
    MeanLowerVoltageError,
    MaxUpperVoltageError,
    MinLowerVoltageError,
    MaxLowerVoltageError,
    MinUpperVoltageError
)
from mlpf.loss.torch.metrics.costs import (
    MeanActivePowerCost,
    MeanRelativeActivePowerCost
)
from mlpf.loss.torch.metrics.reactive import (
    MeanReactivePowerError,
    MeanRelativeReactivePowerError,
    MaxReactivePowerError,
    MaxRelativeReactivePowerError,
    MinReactivePowerError,
    MinRelativeReactivePowerError
)


def generate_pf_ppcs() -> List[Dict]:
    net = pn.case118()
    ppc = pp.converter.to_ppc(net, init="flat")

    base_ppc, converged = runpf(ppc, ppopt=ppoption(OUT_ALL=0, VERBOSE=0))

    ppc_list = generate_uniform_ppcs(
        base_ppc,
        how_many=123,
        low=0.9,
        high=1.1
    )

    return ppc_list


def generate_opf_ppcs() -> List[Dict]:
    net = pn.case118()
    ppc = pp.converter.to_ppc(net, init="flat")

    base_ppc, converged = runpf(ppc, ppopt=ppoption(OUT_ALL=0, VERBOSE=0))

    ppc_list = generate_uniform_ppcs(
        base_ppc,
        how_many=6,
        low=0.9,
        high=1.1,
        method="opf"
    )

    return ppc_list


class MetricTest(unittest.TestCase):
    pf_tolerance = 1e-3
    bounds_tolerance = 1e-6
    cost_tolerance = 1
    relative_cost_tolerance = 1e-3

    def assert_metric_numpy(self, metric_description: DataFrame, tolerance: float):
        for metric in metric_description:
            self.assertLess(np.abs(metric_description[metric]["mean"]), tolerance)

    def assert_metric_torch(self, metrics_dict: Dict, tolerance: float):
        for metric_key in metrics_dict:
            self.assertLess(torch.abs(metrics_dict[metric_key]), tolerance)

    def test_numpy_power_flow(self):

        ppc_list = generate_pf_ppcs()

        # ppc -> Data
        pf_data_list = []
        for ppc in tqdm(ppc_list, desc="Converting ppcs to PF data numpy"):
            pf_data_list.append(PowerFlowData(ppc))

        pf_metrics = MultipleMetrics(
            ActivePowerError(),
            ReactivePowerError(),
            RelativeActivePowerError(),
            RelativeReactivePowerError()
        )

        for i in range(len(pf_data_list)):
            pf_metrics.update(pf_data_list[i].target_vector, pf_data_list[i])

        description = pf_metrics.compute().describe()
        self.assert_metric_numpy(description, self.pf_tolerance)

    def test_torch_power_flow(self):
        ppc_list = generate_pf_ppcs()

        # ppc -> Data
        pf_data_list = []
        for ppc in tqdm(ppc_list, desc="Converting ppcs to PF data torch"):
            pf_data_list.append(PowerFlowData(ppc).to_pyg_data(dtype=torch.float64))

        pf_metrics = MetricCollection(
            MeanActivePowerError(),
            MeanRelativeActivePowerError(),
            MeanReactivePowerError(),
            MeanRelativeReactivePowerError()
        )

        loader = DataLoader(pf_data_list, batch_size=len(pf_data_list), shuffle=True)

        for batch in loader:
            pf_metrics(power_flow_predictions=batch.target_vector, batch=batch)

        pf_metrics_dict = pf_metrics.compute()
        self.assert_metric_torch(pf_metrics_dict, self.pf_tolerance)

    def test_numpy_optimal_power_flow(self):
        ppc_list = generate_opf_ppcs()

        # ppc -> Data
        opf_data_list = []
        for ppc in tqdm(ppc_list, desc="Converting ppcs to OPF data numpy"):
            opf_data_list.append(OptimalPowerFlowData(ppc))

        pf_metrics = MultipleMetrics(
            ActivePowerError(),
            ReactivePowerError(),
            RelativeActivePowerError(),
            RelativeReactivePowerError(),
        )

        bounds_metrics = MultipleMetrics(
            UpperVoltageError(),
            LowerVoltageError(),
            UpperActivePowerError(),
            LowerActivePowerError(),
            UpperReactivePowerError(),
            LowerReactivePowerError(),
        )

        cost_metric = ActivePowerCost()

        relative_cost_metric = RelativeActivePowerCost()

        for i in range(len(opf_data_list)):
            pf_metrics.update(opf_data_list[i].target_vector, opf_data_list[i])
            bounds_metrics.update(opf_data_list[i].target_vector, opf_data_list[i])
            cost_metric.update(opf_data_list[i].target_vector, opf_data_list[i])
            relative_cost_metric.update(opf_data_list[i].target_vector, opf_data_list[i])

        pf_description = pf_metrics.compute().describe()
        self.assert_metric_numpy(pf_description, self.pf_tolerance)

        bounds_description = bounds_metrics.compute().describe()
        self.assert_metric_numpy(bounds_description, self.bounds_tolerance)

        costs = cost_metric.compute()
        target_costs = np.array([data.target_cost for data in opf_data_list])
        self.assertLess(np.abs(costs - target_costs).mean(), self.cost_tolerance)

        relative_costs = relative_cost_metric.compute()
        self.assertLess(np.abs(relative_costs - 1).mean(), self.relative_cost_tolerance)

    def test_torch_optimal_power_flow(self):
        ppc_list = generate_opf_ppcs()

        # ppc -> Data
        opf_data_list = []
        for ppc in tqdm(ppc_list, desc="Converting ppcs to OPF data torch"):
            opf_data_list.append(OptimalPowerFlowData(ppc).to_pyg_data(dtype=torch.float64))

        pf_metrics = MetricCollection(
            MeanActivePowerError(),
            MeanRelativeActivePowerError(),
            MeanReactivePowerError(),
            MeanRelativeReactivePowerError(),
            MaxActivePowerError(),
            MaxRelativeActivePowerError(),
            MaxReactivePowerError(),
            MaxRelativeReactivePowerError(),
            MinActivePowerError(),
            MinRelativeActivePowerError(),
            MinReactivePowerError(),
            MinRelativeReactivePowerError()
        )

        bounds_metrics = MetricCollection(
            MeanUpperVoltageError(),
            MeanLowerVoltageError(),

            MeanUpperActivePowerError(),
            MeanLowerActivePowerError(),
            MeanUpperReactivePowerError(),
            MeanLowerReactivePowerError(),

            MaxUpperVoltageError(),
            MinLowerVoltageError(),
            MaxLowerVoltageError(),
            MinUpperVoltageError(),
            MaxUpperReactivePowerError(),
            MinUpperReactivePowerError(),
            MinLowerReactivePowerError(),
            MaxLowerReactivePowerError(),
            MaxUpperActivePowerError(),
            MinUpperActivePowerError(),
            MaxLowerActivePowerError(),
            MinLowerActivePowerError()
        )

        cost_metric = MeanActivePowerCost()
        relative_cost_metric = MeanRelativeActivePowerCost()

        loader = DataLoader(opf_data_list, batch_size=len(opf_data_list), shuffle=True)

        for batch in loader:
            pf_metrics(power_flow_predictions=batch.target_vector, batch=batch)
            bounds_metrics(power_flow_predictions=batch.target_vector, batch=batch)
            cost_metric(power_flow_predictions=batch.target_vector, batch=batch)
            relative_cost_metric(power_flow_predictions=batch.target_vector, batch=batch)

        self.assert_metric_torch(pf_metrics.compute(), self.pf_tolerance)
        self.assert_metric_torch(bounds_metrics.compute(), self.bounds_tolerance)

        target_costs = torch.tensor([data.target_cost for data in opf_data_list])
        self.assertLess(torch.abs(cost_metric.compute() - target_costs.mean()), self.cost_tolerance)

        self.assertLess(torch.abs(relative_cost_metric.compute() - 1), self.relative_cost_tolerance)


if __name__ == '__main__':
    unittest.main()
