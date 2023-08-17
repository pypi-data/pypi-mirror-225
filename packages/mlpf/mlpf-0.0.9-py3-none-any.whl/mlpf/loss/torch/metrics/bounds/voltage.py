from torch import Tensor
from torch_geometric.data import Data
from torchmetrics import MeanMetric, MaxMetric, MinMetric

from mlpf.enumerations.power_flow_ids import PowerFlowFeatureIds
from mlpf.loss.torch.bound_errors import lower_bound_errors, upper_bound_errors
from mlpf.loss.torch.metrics.aggregation_metric import aggregation_metric

UPPER_VOLTAGE_ERROR_STATE_NAME = "upper_voltage_error"
LOWER_VOLTAGE_ERROR_STATE_NAME = "lower_voltage_error"


def voltage_upper_bound_errors(PQVA_prediction: Tensor, batch: Data):
    return upper_bound_errors(
        value=PQVA_prediction[:, PowerFlowFeatureIds.voltage_magnitude],
        value_max=batch.voltages_max
    )


def voltage_lower_bound_errors(PQVA_prediction: Tensor, batch: Data):
    return lower_bound_errors(
        value=PQVA_prediction[:, PowerFlowFeatureIds.voltage_magnitude],
        value_min=batch.voltages_min
    )


@aggregation_metric(state_name=UPPER_VOLTAGE_ERROR_STATE_NAME,
                    state_fn=voltage_upper_bound_errors)
class MeanUpperVoltageError(MeanMetric):
    """
    Mean upper voltage bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_VOLTAGE_ERROR_STATE_NAME,
                    state_fn=voltage_lower_bound_errors)
class MeanLowerVoltageError(MeanMetric):
    """
    Mean lower voltage bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=UPPER_VOLTAGE_ERROR_STATE_NAME,
                    state_fn=voltage_upper_bound_errors)
class MaxUpperVoltageError(MaxMetric):
    """
    Max upper voltage bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_VOLTAGE_ERROR_STATE_NAME,
                    state_fn=voltage_lower_bound_errors)
class MaxLowerVoltageError(MaxMetric):
    """
    Max lower voltage bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=UPPER_VOLTAGE_ERROR_STATE_NAME,
                    state_fn=voltage_upper_bound_errors)
class MinUpperVoltageError(MinMetric):
    """
    Min upper voltage bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@aggregation_metric(state_name=LOWER_VOLTAGE_ERROR_STATE_NAME,
                    state_fn=voltage_lower_bound_errors)
class MinLowerVoltageError(MinMetric):
    """
    Min lower voltage bound error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."
