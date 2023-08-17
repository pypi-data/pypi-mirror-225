import torch

from torch import Tensor
from typing import Dict, Tuple

from mlpf.data.conversion.numpy.optimal_power_flow import extract_voltage_limits_arrays, extract_active_power_limits_arrays, \
    extract_reactive_power_limits_arrays, \
    extract_demand_arrays, extract_cost_coefficients_array


def extract_voltage_limits_tensors(ppc: Dict, dtype: torch.dtype = torch.float64) -> Tuple[Tensor, Tensor]:
    """
    Extract the voltage magnitude limit tensors (in per unit) from the given PPC object. Cast the tensors into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Lower limits, Upper limits)
    """
    voltages_min, voltages_max = extract_voltage_limits_arrays(ppc)

    return torch.tensor(voltages_min, dtype=dtype), torch.tensor(voltages_max, dtype=dtype)


def extract_active_power_limits_tensors(ppc: Dict, dtype: torch.dtype = torch.float64) -> Tuple[Tensor, Tensor]:
    """
    Extract the active power limit tensors (in per unit) from the given PPC object. Cast the tensors into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Lower limits, Upper limits)
    """
    active_powers_min, active_powers_max = extract_active_power_limits_arrays(ppc)

    return torch.tensor(active_powers_min, dtype=dtype), torch.tensor(active_powers_max, dtype=dtype)


def extract_reactive_power_limits_tensors(ppc: Dict, dtype: torch.dtype = torch.float64) -> Tuple[Tensor, Tensor]:
    """
    Extract the reactive power limit tensors (in per unit) from the given PPC object. Cast the tensors into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Lower limits, Upper limits)
    """
    reactive_powers_min, reactive_powers_max = extract_reactive_power_limits_arrays(ppc)

    return torch.tensor(reactive_powers_min, dtype=dtype), torch.tensor(reactive_powers_max, dtype=dtype)


def extract_demand_tensors(ppc: Dict, dtype: torch.dtype = torch.float64) -> Tuple[Tensor, Tensor]:
    """
    Extract the active and reactive power demand tensors (in per unit) from the given PPC object. Cast the tensors into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Torch dtype.
    :return: (Active power demands, Reactive power demands)
    """
    active_power_demands, reactive_power_demands = extract_demand_arrays(ppc)

    return torch.tensor(active_power_demands, dtype=dtype), torch.tensor(reactive_power_demands, dtype=dtype)


def extract_cost_coefficients_tensor(ppc: Dict, dtype: torch.dtype = torch.float64) -> Tensor:
    """
    Extract the cost coefficients from the given PPC object. Cast the coefficients into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: Cost coefficients matrix.
    """
    cost_coefficients = extract_cost_coefficients_array(ppc)

    return torch.tensor(cost_coefficients, dtype=dtype)
