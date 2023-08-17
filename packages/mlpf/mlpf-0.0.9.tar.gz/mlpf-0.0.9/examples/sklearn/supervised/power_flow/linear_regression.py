import random

import numpy as np
import pandapower as pp
import pandapower.networks as pn

from pypower.ppoption import ppoption
from pypower.runpf import runpf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from mlpf.data.data.power_flow import PowerFlowData
from mlpf.data.generate.generate_uniform_data import generate_uniform_ppcs
from mlpf.loss.numpy.metrics.active import ActivePowerError, RelativeActivePowerError
from mlpf.loss.numpy.metrics.metrics import MultipleMetrics
from mlpf.loss.numpy.metrics.reactive import ReactivePowerError, RelativeReactivePowerError
from mlpf.utils.description_format import format_description


def main():
    # Random seeds
    np.random.seed(123)
    random.seed(123)

    # Generate ppcs

    net = pn.case118()
    ppc = pp.converter.to_ppc(net, init="flat")

    base_ppc, converged = runpf(ppc, ppopt=ppoption(OUT_ALL=0, VERBOSE=0))

    ppc_list = generate_uniform_ppcs(
        base_ppc,
        how_many=1000,
        low=0.9,
        high=1.1
    )

    pf_data = [PowerFlowData(ppc) for ppc in tqdm(ppc_list, desc="Converting ppcs to data")]

    data_train, data_val = train_test_split(pf_data, test_size=0.33, random_state=42)

    features_train = np.vstack([data.feature_vector for data in data_train])
    targets_train = np.vstack([data.target_vector for data in data_train])

    features_val = np.vstack([data.feature_vector for data in data_val])
    targets_val = np.vstack([data.target_vector for data in data_val])

    # Model

    backbone = LinearRegression()

    model = make_pipeline(StandardScaler(), backbone)
    model.fit(features_train, targets_train)

    # Evaluation

    predictions_val = model.predict(features_val)

    power_metrics = MultipleMetrics(
        ActivePowerError(),
        RelativeActivePowerError(),
        ReactivePowerError(),
        RelativeReactivePowerError()
    )

    for i in tqdm(range(predictions_val.shape[0]), desc="Calculating metrics"):
        power_metrics.update(predictions_val[i], data_val[i])

    print(f"\nR2 score: {'train':>10} = {model.score(features_train, targets_train):3.4f}\nR2 score: {'validation':>10} = {model.score(features_val, targets_val):3.4f}\n")

    description = power_metrics.compute().describe()
    description = format_description(description, power_metrics)

    print(description)


if __name__ == "__main__":
    main()
