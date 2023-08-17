import re

from typing import Any, Dict

from torchmetrics import MetricCollection


def get_unit(metric: Any) -> str:
    """
    Extract the unit of the metric as a string if it exists and wrap it up in square brackets.

    :param metric: Metric.
    :return: String of [unit]
    """
    unit = getattr(metric, 'unit', None)  # get metric unit if it exists
    return f" [{unit}]" if unit is not None else ''


def clean_metric_name(metric_name: str) -> str:
    """
    Add a space before capital letters and then turn everything to lowercase.

    :param metric_name: Name of the metric. Usually the string of the class name.
    :return: Clean name.
    """
    return re.sub(r"(\w)([A-Z])", r"\1 \2", metric_name).lower()
