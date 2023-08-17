import numpy as np

from numpy.typing import DTypeLike, NDArray
from typing import Dict, Tuple

from mlpf.enumerations.bus_table import BusTableIds
from mlpf.enumerations.gencost_table import GeneratorCostTableIds
from mlpf.enumerations.generator_table import GeneratorTableIds


def _zero_padding(indices: NDArray, values: NDArray, size: int) -> NDArray:
    """
    Insert values at indices and zeros elsewhere.

    :param indices: Indices array, same size as values.
    :param values: Values array, same size as indices.
    :param size: How big is the final array.
    :return: Zero padded values.
    """
    shape = list(values.shape)
    shape[0] = size
    shape = tuple(shape)

    zero_padded_values = np.zeros(shape)
    zero_padded_values[indices] = values

    return zero_padded_values


def extract_demand_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray]:
    """
    Extract the active and reactive power demand arrays (in per unit) from the given PPC object. Cast the arrays into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Active power demands, Reactive power demands)
    """
    active_power_demands = ppc["bus"][:, BusTableIds.active_power_MW] / ppc["baseMVA"]
    reactive_power_demands = ppc["bus"][:, BusTableIds.reactive_power_MVAr] / ppc["baseMVA"]

    return active_power_demands.astype(dtype), reactive_power_demands.astype(dtype)


def _gen_bus_numbers_and_size(ppc: Dict) -> Tuple[NDArray, int]:
    """
    Get the bus numbers of the generator and the total number of buses(size).

    :param ppc: PYPOWER case format object.
    :return: (gen_bus_numbers, size)
    """
    gen_bus_numbers = ppc["gen"][:, GeneratorTableIds.bus_number].astype(int)

    size = ppc["bus"].shape[0]

    return gen_bus_numbers, size


def extract_active_power_limits_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray]:
    """
    Extract the active power limit arrays (in per unit) from the given PPC object. Cast the arrays into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Lower limits, Upper limits)
    """

    if ppc["gen"].shape[0] != len(np.unique(ppc["gen"][:, GeneratorTableIds.bus_number])):
        raise NotImplementedError("Multiple generators per bus are not yet supported.")

    active_power_demands, _ = extract_demand_arrays(ppc, dtype=np.float64)

    gen_bus_numbers, size = _gen_bus_numbers_and_size(ppc)

    active_powers_min = _zero_padding(gen_bus_numbers, ppc["gen"][:, GeneratorTableIds.min_active_power_MW], size=size) / ppc["baseMVA"] - active_power_demands
    active_powers_max = _zero_padding(gen_bus_numbers, ppc["gen"][:, GeneratorTableIds.max_active_power_MW], size=size) / ppc["baseMVA"] - active_power_demands

    assert (active_powers_min <= active_powers_max).all()

    return active_powers_min.astype(dtype), active_powers_max.astype(dtype)


def extract_reactive_power_limits_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray]:
    """
    Extract the reactive power limit arrays (in per unit) from the given PPC object. Cast the arrays into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Lower limits, Upper limits)
    """

    if ppc["gen"].shape[0] != len(np.unique(ppc["gen"][:, GeneratorTableIds.bus_number])):
        raise NotImplementedError("Multiple generators per bus are not yet supported.")

    _, reactive_power_demands = extract_demand_arrays(ppc, dtype=np.float64)

    gen_bus_numbers, size = _gen_bus_numbers_and_size(ppc)

    reactive_powers_min = _zero_padding(gen_bus_numbers, ppc["gen"][:, GeneratorTableIds.min_reactive_power_MVAr], size=size) / ppc["baseMVA"] - reactive_power_demands
    reactive_powers_max = _zero_padding(gen_bus_numbers, ppc["gen"][:, GeneratorTableIds.max_reactive_power_MVAr], size=size) / ppc["baseMVA"] - reactive_power_demands

    assert (reactive_powers_min <= reactive_powers_max).all()

    return reactive_powers_min.astype(dtype), reactive_powers_max.astype(dtype)


def extract_voltage_limits_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray]:
    """
    Extract the voltage magnitude limit arrays (in per unit) from the given PPC object. Cast the arrays into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Lower limits, Upper limits)
    """
    voltages_min = ppc["bus"][:, BusTableIds.voltage_min_pu]
    voltages_max = ppc["bus"][:, BusTableIds.voltage_max_pu]

    assert (voltages_min <= voltages_max).all()

    return voltages_min.astype(dtype), voltages_max.astype(dtype)


def extract_cost_coefficients_array(ppc: Dict, dtype: DTypeLike = np.float64) -> NDArray:
    """
    Extract the cost coefficients from the given PPC object. Cast the coefficients into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: Cost coefficients matrix.
    """
    gen_bus_numbers, size = _gen_bus_numbers_and_size(ppc)

    # TODO only supports costs for active power
    cost_coefficients = _zero_padding(gen_bus_numbers, ppc["gencost"][:, GeneratorCostTableIds.coefficients_start:], size=size)

    return cost_coefficients.astype(dtype)
