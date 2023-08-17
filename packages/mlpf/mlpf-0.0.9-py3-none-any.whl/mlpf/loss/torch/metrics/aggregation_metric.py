from typing import Callable

import torch

from torch import Tensor
from torch_geometric.data import Data

from mlpf.loss.torch.metrics.utils import incorporate_predictions


def aggregation_metric(state_name: str,
                       state_fn: Callable[[Tensor, Data], Tensor]):
    """
    A decorator that adds methods to a group of metrics that will be use aggregation state values to form metrics.
    This decorator writes some of the boilerplate code.

    :param state_name: Name of the state to be used by torchmetrics. Should be unique. Torchmetrics will calculate the
    state only once per update call in case multiple metrics use it, which they will.
    :param state_fn: A function that calculates the aforementioned state.
    :return: The add_method wrapper.
    """

    def add_methods(cls):
        cls.base_init = cls.__init__  # get Metric constructor
        cls.base_update = cls.update  # Metric update

        def init(self):
            """
            Call the Metric constructor and initialize the states.
            :param self:
            :return:
            """
            self.base_init()

            self.add_state(self.state_name, default=torch.tensor(0.0))
            self.add_state("PQVA_prediction", default=torch.tensor(0.0))

        def update(self, power_flow_predictions: Tensor, batch: Data):
            """
            Update the state and the aggregation metric.

            :param self: Class instance.
            :param power_flow_predictions: Model output.
            :param batch: Data batch.
            :return:
            """
            self.PQVA_prediction = incorporate_predictions(power_flow_predictions, batch)

            self.__setattr__(self.state_name, self.state_fn(self.PQVA_prediction, batch))

            self.base_update(value=self.value_fn(batch))

        cls.full_state_update = True  # the metric requires the previous state value.

        # set the methods
        cls.state_name = state_name

        cls.__init__ = init
        cls.update = update

        cls.state_fn = lambda self, *args: state_fn(*args)
        cls.value_fn = lambda self, batch: self.__getattribute__(self.state_name)  # by default the value function is the state

        return cls

    return add_methods


def custom_value_fn(value_fn: Callable[[Tensor, Tensor, Data], Tensor]):
    """
    Add a custom value function to the aggregation metric. The value function is by default the state.

    :param value_fn: Custom value function.
    :return:
    """

    def add_value_fn(cls):
        cls.value_fn = lambda self, batch: value_fn(self.__getattribute__(self.state_name), self.PQVA_prediction, batch)
        return cls

    return add_value_fn
