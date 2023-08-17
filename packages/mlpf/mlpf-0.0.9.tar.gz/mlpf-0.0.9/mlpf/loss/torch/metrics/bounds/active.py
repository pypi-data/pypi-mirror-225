from torch import Tensor
from torch_geometric.data import Data
from torchmetrics import MeanMetric, MaxMetric, MinMetric

from mlpf.enumerations.power_flow_ids import PowerFlowFeatureIds
from mlpf.loss.torch.bound_errors import lower_bound_errors, upper_bound_errors
from mlpf.loss.torch.metrics.aggregation_metric import aggregation_metric

UPPER_ACTIVE_POWER_ERROR_STATE_NAME = "upper_active_power_error"
LOWER_ACTIVE_POWER_ERROR_STATE_NAME = "lower_active_power_error"


def active_power_upper_bound_errors(PQVA_prediction: Tensor, batch: Data):
    return upper_bound_errors(
        value=PQVA_prediction[:, PowerFlowFeatureIds.active_power],
        value_max=batch.active_powers_max
    )


def active_power_lower_bound_errors(PQVA_prediction: Tensor, batch: Data):
    return lower_bound_errors(
        value=PQVA_prediction[:, PowerFlowFeatureIds.active_power],
        value_min=batch.active_powers_min
    )


@aggregation_metric(state_name=UPPER_ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=active_power_upper_bound_errors)
class MeanUpperActivePowerError(MeanMetric):
    """
    Mean upper active power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=active_power_lower_bound_errors)
class MeanLowerActivePowerError(MeanMetric):
    """
    Mean lower active power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=UPPER_ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=active_power_upper_bound_errors)
class MaxUpperActivePowerError(MaxMetric):
    """
    Max upper active power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=active_power_lower_bound_errors)
class MaxLowerActivePowerError(MaxMetric):
    """
    Max lower active power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=UPPER_ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=active_power_upper_bound_errors)
class MinUpperActivePowerError(MinMetric):
    """
    Min upper active power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=active_power_lower_bound_errors)
class MinLowerActivePowerError(MinMetric):
    """
    Min lower active power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."
