import copy

import numpy as np
import pandapower as pp
import pandapower.networks as pn

from pypower.ppoption import ppoption
from pypower.runopf import runopf

from mlpf.data.conversion.numpy.optimal_power_flow import (
    extract_active_power_limits_arrays,
    extract_cost_coefficients_array,
    extract_demand_arrays,
    extract_reactive_power_limits_arrays,
    extract_voltage_limits_arrays,
)

from mlpf.data.conversion.numpy.power_flow import (
    extract_power_arrays,
    extract_voltage_arrays
)

from mlpf.loss.numpy.bound_errors import (
    lower_bound_errors,
    upper_bound_errors
)

from mlpf.loss.numpy.costs import polynomial_costs

# create and solve PPC
net = pn.case118()
ppc = pp.converter.to_ppc(net, init="flat")

ppopt = ppoption(OUT_ALL=0, VERBOSE=0)
ppc = runopf(copy.deepcopy(ppc), ppopt=ppopt)

# extract quantities
active_powers, reactive_powers = extract_power_arrays(ppc)
voltage_magnitudes, voltage_angles = extract_voltage_arrays(ppc)

voltages_min, voltages_max = extract_voltage_limits_arrays(ppc)
active_powers_min, active_powers_max = extract_active_power_limits_arrays(ppc)
reactive_powers_min, reactive_powers_max = extract_reactive_power_limits_arrays(ppc)

active_power_demands, _ = extract_demand_arrays(ppc)
active_powers_generation = (active_powers + active_power_demands) * ppc["baseMVA"]

cost_coefficients = extract_cost_coefficients_array(ppc)

# calculate errors
voltage_upper_errors = upper_bound_errors(voltage_magnitudes, voltages_max)
voltage_lower_errors = lower_bound_errors(voltage_magnitudes, voltages_min)

active_upper_errors = upper_bound_errors(active_powers, active_powers_max)
active_lower_errors = lower_bound_errors(active_powers, active_powers_min)

reactive_upper_errors = upper_bound_errors(reactive_powers, reactive_powers_max)
reactive_lower_errors = lower_bound_errors(reactive_powers, reactive_powers_min)

cost_errors = np.sum(polynomial_costs(active_powers_generation, cost_coefficients)) - ppc["f"]

print(f"Total V max violation = {np.sum(voltage_upper_errors):.3e} p.u.")
print(f"Total V min violation = {np.sum(voltage_lower_errors):.3e} p.u.")

print(f"Total P max violation = {np.sum(active_upper_errors):.3e} p.u.")
print(f"Total P min violation = {np.sum(active_lower_errors):.3e} p.u.")

print(f"Total Q max violation = {np.sum(reactive_upper_errors):.3e} p.u.")
print(f"Total Q min violation = {np.sum(reactive_lower_errors):.3e} p.u.")

print(f"Total costs = {cost_errors:.3e} $/h")
