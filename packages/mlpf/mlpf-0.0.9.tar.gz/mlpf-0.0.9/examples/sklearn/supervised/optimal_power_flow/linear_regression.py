import random

import numpy as np

from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from mlpf.data.data.optimal_power_flow import OptimalPowerFlowData
from mlpf.data.loading.load_data import load_data
from mlpf.loss.numpy.metrics.active import ActivePowerError, RelativeActivePowerError
from mlpf.loss.numpy.metrics.bounds.active import UpperActivePowerError, LowerActivePowerError
from mlpf.loss.numpy.metrics.bounds.reactive import UpperReactivePowerError, LowerReactivePowerError
from mlpf.loss.numpy.metrics.bounds.voltage import UpperVoltageError, LowerVoltageError
from mlpf.loss.numpy.metrics.costs import ActivePowerCost, RelativeActivePowerCost
from mlpf.loss.numpy.metrics.metrics import MultipleMetrics
from mlpf.loss.numpy.metrics.reactive import ReactivePowerError, RelativeReactivePowerError
from mlpf.utils.description_format import format_description


def main():
    # Random seeds
    np.random.seed(123)
    random.seed(123)

    ppc_list = load_data("solved_opf_ppcs_case118_10k", max_samples=1000)

    # ppc -> Data
    opf_data = [OptimalPowerFlowData(ppc) for ppc in tqdm(ppc_list, desc="Converting ppcs to data")]

    data_train, data_val = train_test_split(opf_data, test_size=0.33, random_state=42)

    features_train = np.vstack([data.feature_vector for data in data_train])
    targets_train = np.vstack([data.target_vector for data in data_train])

    features_val = np.vstack([data.feature_vector for data in data_val])
    targets_val = np.vstack([data.target_vector for data in data_val])

    # Model

    backbone = Ridge()
    model = make_pipeline(StandardScaler(), backbone)
    model.fit(features_train, targets_train)

    # Evaluation

    predictions_val = model.predict(features_val)

    power_metrics = MultipleMetrics(
        ActivePowerError(),
        ReactivePowerError(),
        RelativeActivePowerError(),
        RelativeReactivePowerError(),
        ActivePowerCost(),
        RelativeActivePowerCost(),
        UpperVoltageError(),
        LowerVoltageError(),
        UpperActivePowerError(),
        LowerActivePowerError(),
        UpperReactivePowerError(),
        LowerReactivePowerError()
    )

    for i in tqdm(range(predictions_val.shape[0]), desc="Calculating metrics"):
        power_metrics.update(predictions_val[i], data_val[i])

    print(f"\nR2 score: {'train':>10} = {model.score(features_train, targets_train):3.4f}\nR2 score: {'validation':>10} = {model.score(features_val, targets_val):3.4f}\n")

    description = power_metrics.compute().describe()
    description = format_description(description, power_metrics)

    print(description)


if __name__ == "__main__":
    main()
