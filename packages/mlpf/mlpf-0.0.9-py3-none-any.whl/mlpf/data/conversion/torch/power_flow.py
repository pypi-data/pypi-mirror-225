from typing import Dict, Tuple

import torch
from torch import LongTensor, Tensor

from mlpf.data.conversion.numpy.power_flow import extract_power_arrays, extract_voltage_arrays, extract_line_arrays


def extract_power_tensors(ppc: Dict, dtype: torch.dtype = torch.float32) -> Tuple[Tensor, Tensor]:
    """
    Extract the active and reactive power tensors (in per unit) from the given PPC object. Cast the tensors into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Active powers, Reactive powers)
    """
    active_powers, reactive_powers = extract_power_arrays(ppc)

    return torch.tensor(active_powers, dtype=dtype), torch.tensor(reactive_powers, dtype=dtype)


def extract_voltage_tensors(ppc: Dict, dtype: torch.dtype = torch.float32) -> Tuple[Tensor, Tensor]:
    """
    Extract the voltage magnitude (in per unit) and angle (in radians) tensors from the given PPC object. Cast the tensors into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Voltage magnitudes, Voltage angles)
    """
    voltage_magnitudes, voltage_angles = extract_voltage_arrays(ppc)

    return torch.tensor(voltage_magnitudes, dtype=dtype), torch.tensor(voltage_angles, dtype=dtype)


def extract_line_tensors(ppc: Dict, dtype: torch.dtype = torch.float32) -> Tuple[LongTensor, Tensor, Tensor]:
    """
    Extract the edge index(edge list) and admittance matrix conductance and susceptance tensors (in per unit) from the given PPC object.
    Cast the conductances and susceptances into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Edge index, Conductances, Susceptances)
    """
    edge_index, conductances, susceptances = extract_line_arrays(ppc)

    return torch.LongTensor(edge_index), torch.tensor(conductances, dtype=dtype), torch.tensor(susceptances, dtype=dtype)
