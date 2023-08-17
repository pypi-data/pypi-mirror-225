import copy

import numpy as np
import pandapower as pp
import pandapower.networks as pn

from pypower.ppoption import ppoption
from pypower.runpf import runpf

from mlpf.data.conversion.numpy.power_flow import (
    extract_line_arrays,
    extract_power_arrays,
    extract_voltage_arrays
)

from mlpf.loss.numpy.power_flow import (
    active_power_errors,
    reactive_power_errors
)

net = pn.case118()

ppc = pp.converter.to_ppc(net, init="flat")

ppopt = ppoption(OUT_ALL=0, VERBOSE=0)
ppc, converged = runpf(copy.deepcopy(ppc), ppopt=ppopt)

active_powers, reactive_powers = extract_power_arrays(ppc)
voltage_magnitudes, voltage_angles = extract_voltage_arrays(ppc)
edge_index, conductances, susceptances = extract_line_arrays(ppc)

active_errors = active_power_errors(edge_index, active_powers, voltage_magnitudes, voltage_angles, conductances, susceptances)
reactive_errors = reactive_power_errors(edge_index, reactive_powers, voltage_magnitudes, voltage_angles, conductances, susceptances)

print(f"Total P loss = {np.sum(active_errors):.3e} p.u.")
print(f"Total Q loss = {np.sum(reactive_errors):.3e} p.u.")
