import warnings

import numpy as np

from numpy.typing import DTypeLike, NDArray
from pypower.makeSbus import makeSbus
from pypower.makeYbus import makeYbus
from typing import Dict, Tuple

from mlpf.enumerations.bus_table import BusTableIds


def extract_power_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray]:
    """
    Extract the active and reactive power arrays (in per unit) from the given PPC object. Cast the arrays into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Active powers, Reactive powers)
    """
    complex_power = makeSbus(ppc['baseMVA'], ppc['bus'], ppc['gen'])

    active_powers_pu = np.real(complex_power).astype(dtype)
    reactive_powers_pu = np.imag(complex_power).astype(dtype)

    return active_powers_pu, reactive_powers_pu


def extract_voltage_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray]:
    """
    Extract the voltage magnitude (in per unit) and angle (in radians) arrays from the given PPC object. Cast the arrays into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Voltage magnitudes, Voltage angles)
    """
    # extract voltages and angles
    voltage_magnitudes_pu = ppc['bus'][:, BusTableIds.voltage_magnitude_pu].astype(dtype)
    voltage_angles_deg = ppc['bus'][:, BusTableIds.voltage_angle_deg]
    voltage_angles_rad = np.deg2rad(voltage_angles_deg).astype(dtype)

    return voltage_magnitudes_pu, voltage_angles_rad


def extract_line_arrays(ppc: Dict, dtype: DTypeLike = np.float64) -> Tuple[NDArray, NDArray, NDArray]:
    """
    Extract the edge index(edge list) and admittance matrix conductance and susceptance arrays (in per unit) from the given PPC object.
    Cast the conductances and susceptances into the provided dtype.

    :param ppc: PYPOWER case format object.
    :param dtype: Numpy dtype.
    :return: (Edge index, Conductances, Susceptances)
    """
    warnings.filterwarnings("ignore", message="Casting complex values to real discards the imaginary part")

    # extract edges
    Y_sparse_matrix, _, _ = makeYbus(ppc['baseMVA'], ppc['bus'], ppc['branch'])

    source, target = Y_sparse_matrix.nonzero()
    line_admittances = np.array(Y_sparse_matrix[source, target]).squeeze()

    conductances_pu = np.real(line_admittances).astype(dtype)
    susceptances_pu = np.imag(line_admittances).astype(dtype)

    edge_index = np.vstack((source, target)).astype(np.int64)

    return edge_index, conductances_pu, susceptances_pu
