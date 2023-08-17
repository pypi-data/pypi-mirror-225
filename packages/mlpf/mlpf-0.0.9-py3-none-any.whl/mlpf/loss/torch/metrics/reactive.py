import torch

from torch import Tensor
from torchmetrics import MeanMetric, MaxMetric, MinMetric
from torch_geometric.data import Data

from mlpf.enumerations.power_flow_ids import PowerFlowFeatureIds
from mlpf.loss.relative_values import relative_values
from mlpf.loss.torch.metrics.aggregation_metric import aggregation_metric, custom_value_fn
from mlpf.loss.torch.power_flow import reactive_power_errors

REACTIVE_POWER_ERROR_STATE_NAME = "reactive_power_error"


def absolute_reactive_power_errors(PQVA_prediction: Tensor, batch: Data) -> Tensor:
    """
    Calculate the absolute reactive power errors from the model output and the info from the data batch.

    :param PQVA_prediction: Model output.
    :param batch: Data batch.
    :return: Absolute reactive power errors.
    """

    return torch.abs(
        reactive_power_errors(
            edge_index=batch.edge_index,
            reactive_powers=PQVA_prediction[:, PowerFlowFeatureIds.reactive_power],
            voltages=PQVA_prediction[:, PowerFlowFeatureIds.voltage_magnitude],
            angles_rad=PQVA_prediction[:, PowerFlowFeatureIds.voltage_angle],
            conductances=batch.conductances,
            susceptances=batch.susceptances
        )
    )


def relative_absolute_reactive_power_errors(absolute_reactive_errors: Tensor, PQVA_prediction: Tensor, batch: Data) -> Tensor:
    """
    Calculate the relative absolute reactive power errors.

    :param absolute_reactive_errors: Absolute reactive power errors.
    :param PQVA_prediction: Model output.
    :param batch: Not used but provided for compatibility reasons.
    :return: Relative absolute reactive power errors.
    """

    return relative_values(
        absolute_reactive_errors,
        torch.abs(PQVA_prediction[:, PowerFlowFeatureIds.reactive_power])
    )


@aggregation_metric(state_name=REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=absolute_reactive_power_errors)
class MeanReactivePowerError(MeanMetric):
    """
    Mean absolute reactive power error.
    """

    is_differentiable: bool = True
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@custom_value_fn(value_fn=relative_absolute_reactive_power_errors)
class MeanRelativeReactivePowerError(MeanReactivePowerError):
    """
    Mean relative absolute reactive power error.
    """

    @property
    def unit(self) -> str:
        return "ratio"


@aggregation_metric(state_name=REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=absolute_reactive_power_errors)
class MaxReactivePowerError(MaxMetric):
    """
    Max absolute reactive power error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@custom_value_fn(value_fn=relative_absolute_reactive_power_errors)
class MaxRelativeReactivePowerError(MaxReactivePowerError):
    """
    Max relative absolute reactive power error.
    """

    @property
    def unit(self) -> str:
        return "ratio"


@aggregation_metric(state_name=REACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=absolute_reactive_power_errors)
class MinReactivePowerError(MinMetric):
    """
    Min absolute reactive power error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@custom_value_fn(value_fn=relative_absolute_reactive_power_errors)
class MinRelativeReactivePowerError(MinReactivePowerError):
    """
    Min relative absolute reactive power error.
    """

    @property
    def unit(self) -> str:
        return "ratio"
