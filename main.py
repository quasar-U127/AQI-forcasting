import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from aqi import transform_aqi
from forecasting import trainer


def analyse(df: pd.DataFrame):
    fig, ax = plt.subplots()
    # fig,ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    trend = df["aqi"].rolling(window="365D",
                              min_periods=50).mean()
    ax.plot(trend[365:], label="aqi")
    # ax.set_yticks(np.arange(0, 400, 50.0))
    ax.set_xlabel("Date")
    # ax.set_x
    ax.set_ylabel("aqi")
    fig.savefig("aqi_{}.png".format("trend"))
    plt.close(fig)

    fig, ax = plt.subplots()
    df["aqi"] = pd.to_numeric(df["aqi"])
    seasonal = df["aqi"].rolling(window="90D",
                                 min_periods=30, center=True).mean() - trend
    # fig,ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    ax.plot(seasonal, label="aqi")
    # ax.set_yticks(np.arange(0, 400, 50.0))
    ax.set_xlabel("Date")
    # ax.set_x
    ax.set_ylabel("aqi")
    fig.savefig("aqi_{}.png".format("seasonal"))
    plt.close(fig)

    fig, ax = plt.subplots()
    # fig,ax = plt.subplots(figsize=(5, 2.7), layout='constrained')
    # remaining = df["aqi"] -trend
    remaining_std = (df["aqi"] - seasonal - trend).rolling(window="60D",
                                                            min_periods=30, center=True).std()
    ax.plot(remaining_std, label="aqi")
    # ax.plot(remaining[-1000:-200], label="aqi")
    # ax.set_yticks(np.arange(0, 400, 50.0))
    ax.set_xlabel("Date")
    # ax.set_x
    ax.set_ylabel("aqi")
    fig.savefig("aqi_{}.png".format("remaining_std"))
    plt.close(fig)


def AQI_Convert(df: pd.DataFrame):

    df = df.apply(transform_aqi, axis=1)
    df.to_csv(os.path.join("AQI", "aqi.csv"))
    return df


def preprocessing():
    data = os.path.join(
        "AQI", "nehru-nagar, kanpur-air-quality.csv")
    # data = os.path.join("AQI", "kanpur_preprocessed.csv")
    preprocessed = pd.read_csv(data)
    preprocessed["date"] = pd.to_datetime(preprocessed["date"])

    preprocessed = preprocessed.sort_values(by="date")
    # preprocessed = preprocessed.sort_values(by="date",ascending=False)
    preprocessed = preprocessed.reset_index(drop=True)
    preprocessed = preprocessed.set_index("date")
    preprocessed = preprocessed.replace(" ", "")
    preprocessed = AQI_Convert(preprocessed)
    print(preprocessed.head())
    # print(preprocessed.head(20))
    # get_fft(preprocessed)


def main():
    aqi_data = pd.read_csv(os.path.join("AQI", "aqi.csv"))
    aqi_data["date"] = pd.to_datetime(aqi_data["date"])
    aqi_data = aqi_data.set_index("date")
    # analyse(aqi_data)
    trainer(aqi_data[["aqi"]])


if __name__ == "__main__":
    main()
