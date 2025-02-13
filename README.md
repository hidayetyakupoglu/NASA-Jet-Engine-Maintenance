# Prognostic and Predictive Maintenance (PdM) of NASA Turbofan Jet Engine

Predictive Maintenance techniques are used to determine the condition of an equipment to plan the maintenance/failure ahead of its time. This is very useful as the overall equipment and downtime costs can be reduced significantly.

The objective of this project is to implement various Predictive Maintenance methods and assess the performance of each. Each method can be classified broadly into four categories.

1. Classification: Predicting the failure of machine in upcoming n days
2. Regression: Predicting the remaining useful life of a machine (RUL)
3. Anomaly Detection: Unsupervised learning
4. Component or system survival analysis

## Data
Data sets consists of multiple multivariate time series. Each time series is from a different engine – i.e., the data can be considered to be from a fleet of engines of the same type. You can find the data [here](https://www.kaggle.com/datasets/behrad3d/nasa-cmaps).

The engine is operating normally at the start of each time series, and develops a fault at some point during the series. In the training set, the fault grows in magnitude until system failure. In the test set, the time series ends some time prior to system failure.

Imbalanced class distribution is a common issue in many classification tasks. It is not unusual that the training data contains highly imbalanced positive/negative examples which however reflects the true class distribution in a general population. In predictive maintenance applications, this issue exists: the imbalance of failure events to normal operation events. This issue is due to following two major reasons. First, the failure events usually rarely occurs compared to normal operation state for an in-service asset. Second, there are too few failure events. The business cannot afford to let the asset run-to-failure, as it is at the cost of equipment damage and equipment down time.

The SMOTE module is created based on algorithm "SMOTE: synthetic minority over-sampling technique" [[5]](#5). It is used to increase the size of the minority examples in a data set by synthesizing new examples with minority class. SMOTE module has two parameters: "SMOTE percentage" and "Number of nearest neighbors". The parameter "SMOTE percentage" should be in multiples of hundreds (100,200,300,400,…). This is fraction of new minority examples that gets added. For examples, we double our minority class by setting the value to 100, we triple the size of minority class by setting the value to 200, etc. The parameter "Number of nearest neighbors" is used to generate new examples from minority class. Each generated example is an average of the original example and its nearest neighbors from the same class.

## EDA

## Models for Predictive Maintenance

- Linear, Piecewise-Linear, Exponential Degradation, and ARIMA model for RUL Prediction
- Pattern similarity based forecasting
- Similarity-based model for RUL Prediction
- LSTM model for RUL Prediction and binary and multiclass classification
- RNN model for binary and multiclass classification
- 1D CNN for binary and multiclass classification
- 1D CNN-RNN for binary and multiclass classification
- 1D CNN-GRU for binary and multiclass classification
- 1D CNN-LSTM for binary and multiclass classification
- 1D CNN-SVM for binary classification
- Attention in GRU
- Logistic regression classification
- K nearest neighbors classification
- Support vector machines (linear and RBF kernels) classifiers and regressors
- Naive Bayes and Bayesian Network Models
- Decision trees classification
- Ensembles of DT (random forest, xgboost, light gradient boosting machines) classifiers and regressors
- Autokeras failure prediction
- Tsfresh, sktime, scikit-time
- DTW and Time series clustering
- Genetic Algorithm
- Hidden Markov Models
- Survival Analysis - gradient boosting survival, random survival forest, survival support vector machines
- Autoencoder - Anamaly Detection
- Mulivariant Gaussian Unsupervised Learning
- Bayesian Structural Time Series (BSTS)

# N-CMAPSS_DL
DL evaluation on N-CMAPSS
Turbo fan engine           |  CMAPSS [[1]](#1)
:----------------------------:|:----------------------:
![](turbo_engine.jpg)  |  ![](cmapss.png)

## Sample creator
Following the below instruction, you can create training/test sample arrays for machine learning model (especially for DL architectures that allow time-windowed data as input) from NASA's N-CMAPSS datafile. <br/>
Please download Turbofan Engine Degradation Simulation Data Set-2, so called N-CMAPSS dataset [[2]](#2), from [NASA's prognostic data repository](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/) <br/>
In the downloaded dataset, dataset DS01 has been used for the application of model-based diagnostics and dataset DS02 has been used for data-driven prognostics.   Therefore, we need only dataset DS02. <br/>
Please locate "N-CMAPSS_DS02-006.h5"file to /N-CMAPSS folder. <br/>
Then, you can get npz files for each of 9 engines by running the python codes below.
```bash
python3 sample_creator_unit_auto.py -w 50 -s 1 --test 0 --sampling 10
```
After that, you should run
```bash
python3 sample_creator_unit_auto.py -w 50 -s 1 --test 1 --sampling 10
```
&ndash;  w : window length <br/>
&ndash;  s : stride of window <br/>
&ndash;  test : select train or test, if it is zero, then the code extracts samples from the engines used for training. Otherwise, it creates samples from test engines<br/>
&ndash;  sampling : subsampling the data before creating the output array so that we can set assume different sampling rate to mitigate memory issues.


Please note that we used N = 6 units (u = 2, 5, 10, 16, 18 & 20) for training and M = 3  units (u = 11, 14 & 15) for test, same as for the setting used in [[3]](#3). <br/>

The size of the dataset is significantly large and it can cause memory issues by excessive memory use. Considering memory limitation that may occur when you load and create the samples, we set the data type as 'np.float32' to reduce the size of the data while the data type of the original data is 'np.float64'. Based on our experiments, this does not much affect to the performance when you use the data to train a DL network. If you want to change the type, please check 'data_preparation_unit.py' file in /utils folder.  <br/>

In addition, we offer the data subsampling to handle 'out-of-memory' issues from the given dataset that use the sampling rate of 1Hz. When you set this subsampling input as 10, then it indicates you only take only 1 sample for every 10, the sampling rate is then 0.1Hz.

Finally, you can have 9 npz file in /N-CMAPSS/Samples_whole folder. <br/>

Each compressed file contains two arrays with different labels: 'sample' and 'label'. In the case of the test units, 'label' indicates the ground truth RUL of the test units for evaluation.

For instance, one of the created file, Unit2_win50_str1_smp10.npz, its filename indicates that the file consists of a collection of the sliced time series by time window size 50 from the trajectory of engine (unit) 2 with the sampling rate of 0.1Hz. <br/>

## Load created samples
At first, you should load each of the npy files created in /Samples_whole folder. Then, the samples from the different engines should be aggregated.
```bash
def load_part_array_merge (npz_units):
    sample_array_lst = []
    label_array_lst = []
    for npz_unit in npz_units:
        loaded = np.load(npz_unit)
        sample_array_lst.append(loaded['sample'])
        label_array_lst.append(loaded['label'])
    sample_array = np.dstack(sample_array_lst)
    label_array = np.concatenate(label_array_lst)
    sample_array = sample_array.transpose(2, 0, 1)
    return sample_array, label_array
```
The shape of your sample array should be (# of samples from all the units, window size, # of variables)


## References
<a id="1">[1]</a>
Frederick, Dean & DeCastro, Jonathan & Litt, Jonathan. (2007). User's Guide for the Commercial Modular Aero-Propulsion System Simulation (C-MAPSS). NASA Technical Manuscript. 2007–215026.

<a id="2">[2]</a>
Chao, Manuel Arias, Chetan Kulkarni, Kai Goebel, and Olga Fink. "Aircraft Engine Run-to-Failure Dataset under Real Flight Conditions for Prognostics and Diagnostics." Data. 2021; 6(1):5. https://doi.org/10.3390/data6010005

<a id="3">[3]</a>
Chao, Manuel Arias, Chetan Kulkarni, Kai Goebel, and Olga Fink. "Fusing physics-based and deep learning models for prognostics." Reliability Engineering & System Safety 217 (2022): 107961.

<a id="3">[4]</a>
Mo, Hyunho, and Giovanni Iacca. "Multi-Objective Optimization of Extreme Learning Machine for Remaining Useful Life Prediction." EvoApplications, part of EvoStar 2022 (2022), to appear.

https://www.mathworks.com/help/predmaint/ug/rul-estimation-using-rul-estimator-models.html

<a id="5">[5]</a>
N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer (2002). SMOTE: synthetic minority over-sampling technique. Journal of artificial intelligence research, 16(1), 321-357.

