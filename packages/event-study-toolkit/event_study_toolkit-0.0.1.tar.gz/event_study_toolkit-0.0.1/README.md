
# Event Study Toolkit

event-study-toolkit is a package designed for economists and researchers to conduct an event study pertaining to stocks and bonds. 

## Overview

The Event Study Toolkit provides a Python framework to perform event studies. Event studies are empirical investigations that typically focus on the effects of specific events on the stock and/or bond prices of firms. To learn more about event studies, please see the excellent resource by the folks at [Eventstudytools](https://www.eventstudytools.com/introduction-event-study-methodology)

Leveraging the Pandas functionality, this package allows one to design an event study and calculate relevent statistics regarding the study. Furthermore, With this toolkit, researchers can measure the impact of specific events on the stock and/or bond prices of involved firms, control for market movements, and perform various statistical tests. In addition, this package provides access to multiple statistical tests, both parametric and nonparametric.


## Features

1. **Data Preparation**: Easily load and preprocess your data for analysis.
2. **Model Estimation**: Fit your data to different models, both standard and custom, in order to estimate normal returns. Standard models include Market, CAPM, and Fama-French (column names must match up)
3. **Prediction**: Predict returns during the event period.
4. **Abnormal Returns**: Calculate the abnormal returns, which are the actual returns minus the predicted returns.
5. **Cumulative Abnormal Returns**: Group and sum abnormal returns to get cumulative values.
6. **Test Statistics**: Obtain various test statistics on both a full-sample and group-level basis.
7. **Rank-based Tests**: Implement rank-based tests, such as the Generalized Rank Test and the Wilcoxon Rank-Sum Test.

## Usage

Below are brief descriptions of the primary functions and their purposes:

- `fitModel(modelType)`: This function fits the data to the provided model type to estimate normal returns.
  
- `createEvtChunk()`: This function creates chunks or groups of event data for further analysis.
  
- `predictReturn(x, est_params, evt_chunk)`: Given a group and model parameters, this function predicts returns during the event period.
  
- `getPredictedReturns(modelType)`: Retrieves predicted returns for all groups.
  
- `getAbnormalReturns(modelType)`: Calculates abnormal returns for all data.
  
- `getCARS(modelType)`: Returns the Cumulative Abnormal Returns (CARs) by summing abnormal returns for specific groups.

- `t_stat(series)`: Computes the t-statistic for a given series.
  
- `getFullSampleTestStatistic(modelType)`: Returns full sample test statistics for the data.
  
- `getGroupLevelTestStatistics(modelType, GRP)`: Provides test statistics based on groupings specified by the user.

- `getGRANK(modelType, GRP)`: Implements the Generalized Rank Test for the specified group.
  
- `getWilcoxon(modelType, GRP)`: Implements the Wilcoxon Rank-Sum Test for the specified group.

## Getting Started

1. **Installation**:
    Ensure you have all the required libraries installed. This toolkit heavily relies on libraries such as pandas, numpy, and scipy.

2. **Data Preparation**:
    - Prepare your data in a suitable format. Ensure you have columns for unique identifiers, return data, and event dates.
    - Load your data into the toolkit using the available methods.
    
3. **Model Estimation & Prediction**:
    - Choose the model type you wish to use. This toolkit allows for standard models and also offers flexibility for custom models.
    - Predict the returns during the event period using the estimated models.

4. **Analysis**:
    - Compute abnormal and cumulative abnormal returns.
    - Obtain various test statistics, both on a full-sample and group-level basis.

5. **Advanced Testing**:
    If you need more advanced testing, make use of rank-based tests available in the toolkit.

## Contribution

Feel free to contribute to this project by submitting pull requests or raising issues on the project's GitHub page. Ensure you adhere to the code style guidelines of the project.

## License

This project is licensed under the MIT License. Refer to the `LICENSE` file for more details.

---

Created by [Your Name/Team], [Year].


