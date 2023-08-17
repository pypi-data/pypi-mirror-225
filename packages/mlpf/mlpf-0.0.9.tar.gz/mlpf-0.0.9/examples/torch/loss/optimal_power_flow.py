import copy
import torch

import pandapower as pp
import pandapower.networks as pn

from pypower.ppoption import ppoption
from pypower.runopf import runopf

from mlpf.data.conversion.torch.optimal_power_flow import (
    extract_active_power_limits_tensors,
    extract_cost_coefficients_tensor,
    extract_demand_tensors,
    extract_reactive_power_limits_tensors,
    extract_voltage_limits_tensors,
)

from mlpf.data.conversion.torch.power_flow import (
    extract_power_tensors,
    extract_voltage_tensors
)

from mlpf.loss.torch.bound_errors import (
    lower_bound_errors,
    upper_bound_errors
)

from mlpf.loss.torch.costs import polynomial_costs

# create and solve PPC
net = pn.case118()
ppc = pp.converter.to_ppc(net, init="flat")

ppopt = ppoption(OUT_ALL=0, VERBOSE=0)
ppc = runopf(copy.deepcopy(ppc), ppopt=ppopt)

# extract quantities
active_powers, reactive_powers = extract_power_tensors(ppc, dtype=torch.float64)
voltage_magnitudes, voltage_angles = extract_voltage_tensors(ppc, dtype=torch.float64)

voltages_min, voltages_max = extract_voltage_limits_tensors(ppc, dtype=torch.float64)
active_powers_min, active_powers_max = extract_active_power_limits_tensors(ppc, dtype=torch.float64)
reactive_powers_min, reactive_powers_max = extract_reactive_power_limits_tensors(ppc, dtype=torch.float64)

active_power_demands, _ = extract_demand_tensors(ppc, dtype=torch.float64)
active_powers_generation = (active_powers + active_power_demands) * ppc["baseMVA"]

cost_coefficients = extract_cost_coefficients_tensor(ppc, dtype=torch.float64)

# calculate errors
voltage_upper_errors = upper_bound_errors(voltage_magnitudes, voltages_max)
voltage_lower_errors = lower_bound_errors(voltage_magnitudes, voltages_min)

active_upper_errors = upper_bound_errors(active_powers, active_powers_max)
active_lower_errors = lower_bound_errors(active_powers, active_powers_min)

reactive_upper_errors = upper_bound_errors(reactive_powers, reactive_powers_max)
reactive_lower_errors = lower_bound_errors(reactive_powers, reactive_powers_min)

cost_errors = torch.sum(polynomial_costs(active_powers_generation, cost_coefficients)) - ppc["f"]

print(f"Total V max violation = {torch.sum(voltage_upper_errors):.3e} p.u.")
print(f"Total V min violation = {torch.sum(voltage_lower_errors):.3e} p.u.")

print(f"Total P max violation = {torch.sum(active_upper_errors):.3e} p.u.")
print(f"Total P min violation = {torch.sum(active_lower_errors):.3e} p.u.")

print(f"Total Q max violation = {torch.sum(reactive_upper_errors):.3e} p.u.")
print(f"Total Q min violation = {torch.sum(reactive_lower_errors):.3e} p.u.")

print(f"Total costs = {cost_errors:.3e} $/h")
