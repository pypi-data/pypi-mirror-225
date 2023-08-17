import numpy as np
import pandas as pd

from pandas import DataFrame

from mlpf.loss.numpy.metrics.metrics import MultipleMetrics
from mlpf.utils.logging import clean_metric_name


def format_description(description: DataFrame,
                       metrics: MultipleMetrics,
                       metric_unit_width: int = 20,
                       metric_value_width: int = 15,
                       metric_value_decimals: int = 5,
                       metric_name_width: int = 35) -> DataFrame:
    """
    Format the metrics pandas description to look nice in the terminal.

    :param description: From df.describe().
    :param metrics:
    :param metric_unit_width:
    :param metric_value_width:
    :param metric_value_decimals:
    :param metric_name_width:
    :return: Formatted description.
    """
    description = description.drop("count", axis="index").T
    description.insert(loc=0, column="unit", value=np.array([f"{f'[{metric.unit}]':^{metric_unit_width}}" for metric in metrics]))

    pd.set_option('display.width', 1000)
    pd.set_option('colheader_justify', 'center')
    pd.set_option('display.float_format', lambda x: f"{x:^{metric_value_width}.{metric_value_decimals}f}")

    description = description.rename(lambda name: f"{clean_metric_name(name):>{metric_name_width}}", axis="index")

    return description
