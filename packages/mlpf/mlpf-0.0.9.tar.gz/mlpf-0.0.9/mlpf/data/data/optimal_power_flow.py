import torch

import numpy as np

from numpy.typing import DTypeLike
from pypower.ppoption import ppoption
from pypower.runopf import runopf
from torch_geometric.data import Data

from mlpf.data.conversion.numpy.optimal_power_flow import extract_voltage_limits_arrays, extract_active_power_limits_arrays, \
    extract_reactive_power_limits_arrays, extract_demand_arrays, extract_cost_coefficients_array
from mlpf.data.data.power_flow import PowerFlowData


class OptimalPowerFlowData(PowerFlowData):
    """
    A class that holds all the data needed for a machine learning optimal power flow.

    TODO individual field descriptions
    """

    def __init__(self, ppc: dict, solve: bool = False, dtype: DTypeLike = np.float64):
        """
        Extract all the data of the optimal power flow problem into a namespace object. The ppc should have a solved optimal power flow;
        otherwise if solve is set to True, and optimal power flow will be run.

        :param ppc: PYPOWER case object.
        :param solve: To run an OPF solver or not.
        :param dtype: Data type into which to cast the data.
        """
        if solve:
            ppc = runopf(ppc, ppopt=ppoption(OUT_ALL=0, VERBOSE=0))

        super(OptimalPowerFlowData, self).__init__(ppc, dtype=dtype)

        self.voltages_min, self.voltages_max = extract_voltage_limits_arrays(ppc, dtype=dtype)
        self.active_powers_min, self.active_powers_max = extract_active_power_limits_arrays(ppc, dtype=dtype)
        self.reactive_powers_min, self.reactive_powers_max = extract_reactive_power_limits_arrays(ppc, dtype=dtype)

        self.active_power_demands, self.reactive_power_demands = extract_demand_arrays(ppc, dtype=dtype)

        self.cost_coefficients = extract_cost_coefficients_array(ppc, dtype=dtype)

        self.baseMVA = ppc["baseMVA"]
        self.target_cost = ppc.get('f', float('nan'))

    def to_pyg_data(self, dtype: torch.dtype = torch.float32) -> Data:
        """
        Cast the OptimalPowerFlowData object into a PyTorch geometric Data object.

        :param dtype: Torch dtype.
        :return: PyTorch geometric Data object.
        """

        return Data(
            baseMVA=self.baseMVA,

            PQVA_matrix=torch.tensor(self.PQVA_matrix, dtype=dtype),
            PQVA_mask=torch.BoolTensor(self.PQVA_mask),

            voltages_min=torch.tensor(self.voltages_min, dtype=dtype),
            voltages_max=torch.tensor(self.voltages_max, dtype=dtype),

            active_powers_min=torch.tensor(self.active_powers_min, dtype=dtype),
            active_powers_max=torch.tensor(self.active_powers_max, dtype=dtype),

            reactive_powers_min=torch.tensor(self.reactive_powers_min, dtype=dtype),
            reactive_powers_max=torch.tensor(self.reactive_powers_max, dtype=dtype),

            active_power_demands=torch.tensor(self.active_power_demands, dtype=dtype),
            reactive_power_demands=torch.tensor(self.reactive_power_demands, dtype=dtype),

            cost_coefficients=torch.tensor(self.cost_coefficients, dtype=dtype),

            feature_vector=torch.tensor(self.feature_vector, dtype=dtype).unsqueeze(0),

            target_cost=self.target_cost,
            target_vector=torch.tensor(self.target_vector, dtype=dtype).unsqueeze(0),

            conductances=torch.tensor(self.conductances, dtype=dtype),
            susceptances=torch.tensor(self.susceptances, dtype=dtype),

            edge_attr=torch.tensor(self.edge_attr, dtype=dtype),
            edge_index=torch.LongTensor(self.edge_index),
            x=torch.tensor(self.x, dtype=dtype)
        )
