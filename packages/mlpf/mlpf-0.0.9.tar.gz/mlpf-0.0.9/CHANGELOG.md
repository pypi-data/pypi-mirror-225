# Change log

## 0.0.1 (17/06/2023)

First release

## 0.0.5 (19/06/2023)

Add README.md as long description in PyPi.

## 0.0.6 (20/06/2023)

* Configure setup.py such that `pip install mlpf` works.
* Separate torch and numpy in data conversion

## 0.0.7(24/06/2023)

* Refactor power flow errors in such a way that the calculation is now
  separate for active and reactive power decoupling them
* Refactor TorchMetrics custom metrics to return only one metric

## 0.0.8(??/??/2023)

* rename bounds error functions
* move PF/OPF mask functions
* add option to solve OPF when generating data
* extract OPF data
* create metrics for PF and OPF
* unite numpy/torch data objects
* refactor ppc -> (o)pf conversion by splitting it into multiple smaller functions
* removed the functions that create the data objects. Instead, class constructors do that
* remove opf_feature_matrix from OPFData and replace it with the corresponding fields themselves

## 0.0.9(16/08/2023)

* add custom progress bar for examples
* remove ascii=True flag from every tqdm progress bar
* add Min and Max metrics