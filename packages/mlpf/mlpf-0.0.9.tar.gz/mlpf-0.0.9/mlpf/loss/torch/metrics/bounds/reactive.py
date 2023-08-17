from torch import Tensor
from torch_geometric.data import Data
from torchmetrics import MeanMetric, MaxMetric, MinMetric

from mlpf.enumerations.power_flow_ids import PowerFlowFeatureIds
from mlpf.loss.torch.bound_errors import lower_bound_errors, upper_bound_errors
from mlpf.loss.torch.metrics.aggregation_metric import aggregation_metric

UPPER_REACTIVE_POWER_ERROR_STATE_NAME = "upper_reactive_power_error"
LOWER_REACTIVE_POWER_ERROR_STATE_NAME = "lower_reactive_power_error"


def reactive_power_upper_bound_errors(PQVA_prediction: Tensor, batch: Data):
    return upper_bound_errors(
        value=PQVA_prediction[:, PowerFlowFeatureIds.reactive_power],
        value_max=batch.reactive_powers_max
    )


def reactive_power_lower_bound_errors(PQVA_prediction: Tensor, batch: Data):
    return lower_bound_errors(
        value=PQVA_prediction[:, PowerFlowFeatureIds.reactive_power],
        value_min=batch.reactive_powers_min
    )


@aggregation_metric(state_name=UPPER_REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=reactive_power_upper_bound_errors)
class MeanUpperReactivePowerError(MeanMetric):
    """
    Mean upper reactive power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=reactive_power_lower_bound_errors)
class MeanLowerReactivePowerError(MeanMetric):
    """
    Mean lower reactive power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=UPPER_REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=reactive_power_upper_bound_errors)
class MaxUpperReactivePowerError(MaxMetric):
    """
    Max upper reactive power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=reactive_power_lower_bound_errors)
class MaxLowerReactivePowerError(MaxMetric):
    """
    Max lower reactive power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=UPPER_REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=reactive_power_upper_bound_errors)
class MinUpperReactivePowerError(MinMetric):
    """
    Min upper reactive power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=reactive_power_lower_bound_errors)
class MinLowerReactivePowerError(MinMetric):
    """
    Min lower reactive power bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."
