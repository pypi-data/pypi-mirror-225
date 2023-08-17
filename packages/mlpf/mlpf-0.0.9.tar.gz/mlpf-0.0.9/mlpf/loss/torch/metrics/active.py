import torch

from torch import Tensor
from torchmetrics import MeanMetric, MaxMetric, MinMetric
from torch_geometric.data import Data

from mlpf.enumerations.power_flow_ids import PowerFlowFeatureIds
from mlpf.loss.relative_values import relative_values
from mlpf.loss.torch.metrics.aggregation_metric import aggregation_metric, custom_value_fn
from mlpf.loss.torch.power_flow import active_power_errors

ACTIVE_POWER_ERROR_STATE_NAME = "active_power_error"


def absolute_active_power_errors(PQVA_prediction: Tensor, batch: Data) -> Tensor:
    """
    Calculate the absolute active power errors from the model output and the info from the data batch.

    :param PQVA_prediction: Model output.
    :param batch: Data batch.
    :return: Absolute active power errors.
    """
    return torch.abs(
        active_power_errors(
            edge_index=batch.edge_index,
            active_powers=PQVA_prediction[:, PowerFlowFeatureIds.active_power],
            voltages=PQVA_prediction[:, PowerFlowFeatureIds.voltage_magnitude],
            angles_rad=PQVA_prediction[:, PowerFlowFeatureIds.voltage_angle],
            conductances=batch.conductances,
            susceptances=batch.susceptances
        )
    )


def relative_absolute_active_power_errors(absolute_active_errors: Tensor, PQVA_prediction: Tensor, batch: Data) -> Tensor:
    """
    Calculate the relative absolute active power errors.

    :param absolute_active_errors: Absolute active power errors.
    :param PQVA_prediction: Model output.
    :param batch: Not used but provided for compatibility reasons.
    :return: Relative absolute active power errors.
    """
    return relative_values(
        absolute_active_errors,
        torch.abs(PQVA_prediction[:, PowerFlowFeatureIds.active_power])
    )


@aggregation_metric(state_name=ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=absolute_active_power_errors)
class MeanActivePowerError(MeanMetric):
    """
    Mean absolute active power error.
    """

    is_differentiable: bool = True
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@custom_value_fn(value_fn=relative_absolute_active_power_errors)
class MeanRelativeActivePowerError(MeanActivePowerError):
    """
    Mean relative absolute active power error.
    """

    @property
    def unit(self) -> str:
        return "ratio"


@aggregation_metric(state_name=ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=absolute_active_power_errors)
class MaxActivePowerError(MaxMetric):
    """
    Max absolute active power error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@custom_value_fn(value_fn=relative_absolute_active_power_errors)
class MaxRelativeActivePowerError(MaxActivePowerError):
    """
    Max relative absolute active power error.
    """

    @property
    def unit(self) -> str:
        return "ratio"


@aggregation_metric(state_name=ACTIVE_POWER_ERROR_STATE_NAME,
                    state_fn=absolute_active_power_errors)
class MinActivePowerError(MinMetric):
    """
    Min absolute active power error.
    """

    is_differentiable: bool = False
    higher_is_better: bool = False

    @property
    def unit(self) -> str:
        return "p.u."


@custom_value_fn(value_fn=relative_absolute_active_power_errors)
class MinRelativeActivePowerError(MinActivePowerError):
    """
    Min relative absolute active power error.
    """

    @property
    def unit(self) -> str:
        return "ratio"
