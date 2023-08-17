import torch

from torch import Tensor
from torch_geometric.data import Data
from torch_scatter import scatter_sum
from torchmetrics import MeanMetric, MaxMetric, MinMetric

from mlpf.enumerations.power_flow_ids import PowerFlowFeatureIds
from mlpf.loss.relative_values import relative_values
from mlpf.loss.torch.costs import polynomial_costs
from mlpf.loss.torch.metrics.aggregation_metric import aggregation_metric, custom_value_fn

ACTIVE_POWER_COST_STATE_NAME = "active_power_cost"


def calculate_cost(PQVA_prediction: Tensor, batch: Data) -> Tensor:
    """
    Extract the active powers generation, the cost coefficients and baseMVA and use them to calculate the polynomial cost function value.

    :param PQVA_prediction: Model output.
    :param batch: Data batch.
    :return: Per grid cost.
    """
    active_powers = PQVA_prediction[:, PowerFlowFeatureIds.active_power]

    active_powers_generation = (active_powers + batch.active_power_demands) * batch.baseMVA[batch.batch]

    return scatter_sum(polynomial_costs(active_powers_generation, batch.cost_coefficients), index=batch.batch)


def relative_active_power_costs(costs: Tensor, PQVA_prediction: Tensor, batch: Data) -> Tensor:
    """
    Calculate the relative absolute active power costs.

    :param costs: Absolute active power costs.
    :param PQVA_prediction: Model output.
    :param batch: Not used but provided for compatibility reasons.
    :return: Relative absolute active power costs.
    """
    return torch.abs(
        relative_values(
            costs,
            batch.target_cost
        )
    )


@aggregation_metric(state_name=ACTIVE_POWER_COST_STATE_NAME,
                    state_fn=calculate_cost)
class MeanActivePowerCost(MeanMetric):
    """
    Mean active power costs.
    """

    @property
    def unit(self) -> str:
        return "$/h"


@custom_value_fn(value_fn=relative_active_power_costs)
class MeanRelativeActivePowerCost(MeanActivePowerCost):
    """
    Mean relative active power costs.
    """

    @property
    def unit(self) -> str:
        return "ratio"


@aggregation_metric(state_name=ACTIVE_POWER_COST_STATE_NAME,
                    state_fn=calculate_cost)
class MaxActivePowerCost(MaxMetric):
    """
    Max active power costs.
    """

    @property
    def unit(self) -> str:
        return "$/h"


@custom_value_fn(value_fn=relative_active_power_costs)
class MaxRelativeActivePowerCost(MaxActivePowerCost):
    """
    Max relative active power costs.
    """

    @property
    def unit(self) -> str:
        return "ratio"


@aggregation_metric(state_name=ACTIVE_POWER_COST_STATE_NAME,
                    state_fn=calculate_cost)
class MinActivePowerCost(MinMetric):
    """
    Min active power costs.
    """

    @property
    def unit(self) -> str:
        return "$/h"


@custom_value_fn(value_fn=relative_active_power_costs)
class MinRelativeActivePowerCost(MinActivePowerCost):
    """
    Min relative active power costs.
    """

    @property
    def unit(self) -> str:
        return "ratio"
