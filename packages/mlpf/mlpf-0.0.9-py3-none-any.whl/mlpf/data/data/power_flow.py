import torch

import numpy as np

from numpy.typing import DTypeLike
from torch_geometric.data import Data

from mlpf.data.conversion.numpy.power_flow import extract_power_arrays, extract_voltage_arrays, extract_line_arrays
from mlpf.data.masks.power_flow import create_power_flow_feature_mask
from mlpf.enumerations.bus_table import BusTableIds
from mlpf.utils.ppc import ppc_runpf


class PowerFlowData:
    """
    A class that holds all the data needed for a machine learning power flow.

    TODO individual field descriptions
    """

    def __init__(self, ppc: dict, solve: bool = False, dtype: DTypeLike = np.float64):
        """
        Extract all the relevant info from the ppc file as ndarrays and pack it into a PyG Data object.

        :param ppc: PyPower case format object
        :param solve: If True, a power flow calculation in PyPower will be called before extracting info.
        :param dtype: Torch data type to cast the real valued tensors into.
        """
        if solve:
            ppc = ppc_runpf(ppc)

        active_powers, reactive_powers = extract_power_arrays(ppc, dtype=dtype)
        voltage_magnitudes, voltage_angles = extract_voltage_arrays(ppc, dtype=dtype)
        edge_index, conductances, susceptances = extract_line_arrays(ppc, dtype=dtype)

        PQVA_matrix = np.vstack((active_powers, reactive_powers, voltage_magnitudes, voltage_angles)).T

        PQVA_mask = create_power_flow_feature_mask(ppc["bus"][:, BusTableIds.bus_type])

        edge_attributes = np.vstack((conductances, susceptances))

        self.PQVA_matrix = PQVA_matrix
        self.conductances = conductances
        self.edge_attr = edge_attributes
        self.edge_index = edge_index
        self.PQVA_mask = PQVA_mask
        self.susceptances = susceptances
        self.target_vector = PQVA_matrix[~PQVA_mask]

    @property
    def x(self):
        """
        Get the feature matrix x. Overwrite this function to get a different feature vector.
        :return:
        """
        return self.PQVA_matrix

    @property
    def feature_vector(self):
        """
        Get the feature vector of the PowerFlowData object. Overwrite this function to get a different feature vector.
        :return:
        """
        return self.x[self.PQVA_mask]

    def to_pyg_data(self, dtype: torch.dtype = torch.float32) -> Data:
        """
        Cast the PowerFlowData object into a PyTorch geometric Data object.

        :param dtype: Torch dtype.
        :return: PyTorch geometric Data object.
        """
        return Data(
            PQVA_matrix=torch.tensor(self.PQVA_matrix, dtype=dtype),
            conductances=torch.tensor(self.conductances, dtype=dtype),
            edge_attr=torch.tensor(self.edge_attr, dtype=dtype),
            edge_index=torch.LongTensor(self.edge_index),
            PQVA_mask=torch.BoolTensor(self.PQVA_mask),
            feature_vector=torch.tensor(self.feature_vector, dtype=dtype).unsqueeze(0),
            susceptances=torch.tensor(self.susceptances, dtype=dtype),
            target_vector=torch.tensor(self.target_vector, dtype=dtype).unsqueeze(0),
            x=torch.tensor(self.x, dtype=dtype)
        )
