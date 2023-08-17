import copy
import torch

import pandapower as pp
import pandapower.networks as pn

from pypower.ppoption import ppoption
from pypower.runpf import runpf

from mlpf.data.conversion.torch.power_flow import (
    extract_line_tensors,
    extract_power_tensors,
    extract_voltage_tensors
)
from mlpf.loss.torch.power_flow import (
    active_power_errors,
    reactive_power_errors
)

net = pn.case118()

ppc = pp.converter.to_ppc(net, init="flat")

ppopt = ppoption(OUT_ALL=0, VERBOSE=0)
ppc, converged = runpf(copy.deepcopy(ppc), ppopt=ppopt)

# note: going from float64 to float32(the standard in torch) will increase the PF loss significantly
active_powers, reactive_powers = extract_power_tensors(ppc, dtype=torch.float64)
voltage_magnitudes, voltage_angles = extract_voltage_tensors(ppc, dtype=torch.float64)
edge_index, conductances, susceptances = extract_line_tensors(ppc, dtype=torch.float64)

active_errors = active_power_errors(edge_index, active_powers, voltage_magnitudes, voltage_angles, conductances, susceptances)
reactive_errors = reactive_power_errors(edge_index, reactive_powers, voltage_magnitudes, voltage_angles, conductances, susceptances)

print(f"Total P loss = {torch.sum(active_errors):.3e} p.u.")
print(f"Total Q loss = {torch.sum(reactive_errors):.3e} p.u.")
