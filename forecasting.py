from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import TimeSeriesSplit,cross_val_score
import pandas as pd

def prepare_forcasting_data(series:pd.DataFrame):
    series.loc[:, "aqi_yesterday"] = series.loc[:, "aqi"].shift(1)
    series.loc[:, "aqi_diff_1"] = series.loc[:, "aqi_yesterday"].diff(1)
    series.loc[:, "aqi_diff_2"] = series.loc[:, "aqi_diff_1"].shift(1)
    series.loc[:, "aqi_diff_3"] = series.loc[:, "aqi_diff_1"].shift(2)
    series.loc[:, "aqi_diff_4"] = series.loc[:, "aqi_diff_1"].shift(3)
    series.loc[:, "aqi_diff_5"] = series.loc[:, "aqi_diff_1"].shift(4)
    series.loc[:, "aqi_diff_6"] = series.loc[:, "aqi_diff_1"].shift(5)
    series.loc[:, "aqi_diff_7"] = series.loc[:, "aqi_diff_1"].shift(6)
    series.loc[:, "aqi_diff_8"] = series.loc[:, "aqi_diff_1"].shift(7)
    series.loc[:, "aqi_diff_9"] = series.loc[:, "aqi_diff_1"].shift(8)
    series.loc[:, "aqi_yesteryear"] = series.loc[:, "aqi"].shift(365)
    series.loc[:, "aqi_yeardiff_1"] = series.loc[:, "aqi_yesteryear"].diff(365)
    return series

def trainer(series:pd.DataFrame):
    # model = MLPRegressor()
    model = RandomForestRegressor()
    param_search = {
        'n_estimators': [20, 50, 100],
        'max_features': ['auto', 'sqrt', 'log2'],
        'max_depth': [i for i in range(5, 15)]
    }
    series = prepare_forcasting_data(series=series)

    series = series.dropna()
    # trainXY = series[:"2020"]
    trainXY = series
    trainX = trainXY.drop("aqi",axis=1)
    trainY = trainXY["aqi"]

    tscv = TimeSeriesSplit(n_splits=10)
    cv_results = cross_val_score(
        model, trainX, trainY, cv=tscv, scoring='neg_mean_absolute_error')
    print(cv_results)
    model.fit(trainX,trainY)

    testXY = series["2020":]

    