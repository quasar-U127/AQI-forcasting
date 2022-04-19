import math
from typing import Any, Dict, List
import pandas as pd
import numpy as np

Indices_table = {}
Indices_table["AQI_Category"] = ["Good", "Satisfactory",
                                 "Moderately_polluted", "Poor", "Very Poor", "Severe"]
Indices_table["AQI"] = [[0, 50], [51, 100], [
    101, 200], [201, 300], [301, 400], [401, 500]]
Indices_table["pm10"] = [[0, 50], [51, 100], [101, 250],
                         [251, 350], [351, 430], [431, float("infinity")]]
Indices_table["pm25"] = [[0, 30], [31, 60], [61, 90],
                         [91, 120], [121, 250], [250.1, float("infinity")]]
Indices_table["no2"] = [[0, 40], [41, 80], [81, 180], [
    181, 280], [281, 400], [400.1, float("infinity")]]
Indices_table["o3"] = [[0, 50], [51, 100], [101, 168],
                       [169, 208], [209, 748], [748.1, float("infinity")]]
Indices_table["co"] = [[0, 1.0], [1.1, 2.0], [2.1, 10],
                       [10, 17], [17, 34], [34.1, float("infinity")]]
Indices_table["s02"] = [[0, 40], [41, 80], [81, 380], [
    381, 800], [801, 1600], [1600.1, float("infinity")]]
Indices_table["nh3"] = [[0, 200], [201, 400], [401, 800], [
    801, 1200], [1200, 1800], [1800.1, float("infinity")]]
Indices_table["pb"] = [[0, 0.5], [0.5, 1.0], [1.1, 2.0],
                       [2.1, 3.0], [3.1, 3.5], [3.51, float("infinity")]]

Buckets = ["Good", "Satisfactory",
           "Moderately Polluted", "Poor", "Very Poor", "Severe"]


def get_aqi_from_concentration(pollutant: List[List[float]], cp: float):
    if cp is None:
        return cp
    aqi = Indices_table["AQI"]
    for k, interval in enumerate(pollutant):
        if(cp >= pollutant[k][0] and cp <= pollutant[k][1]):
            bphi = pollutant[k][1]
            if(bphi == float("infinity")):
                bphi = cp+0.1
            bplo = pollutant[k][0]
            ihi = aqi[k][1]
            ilo = aqi[k][0]
            subindex = ((ihi-ilo)/(bphi-bplo))*(cp-bplo)+ilo
            return subindex


def transform_aqi(row: Dict[str, Any]):
    num_count = 0
    p = 0
    # pm25 = get_aqi_from_concentration(pollutant=Indices_table["pm25"],cp=row["pm25"])
    pm25 = row["pm25"]
    if not math.isnan(pm25):
        num_count += 1
        p = max(p, pm25)
    pm10 = row["pm10"]
    # pm10 = get_aqi_from_concentration(pollutant=Indices_table["pm10"],cp=row["pm10"])
    if not math.isnan(pm10):
        num_count += 1
        p = max(p, pm10)
    o3 = row["o3"]
    # o3 = get_aqi_from_concentration(pollutant=Indices_table["o3"],cp=row["o3"])
    if not math.isnan(o3):
        num_count += 1
        p = max(p, o3)
    no2 = row["no2"]
    # no2 = get_aqi_from_concentration(pollutant=Indices_table["no2"],cp=row["no2"])
    if not math.isnan(no2):
        num_count += 1
        p = max(p, no2)
    co = row["co"]
    # co = get_aqi_from_concentration(pollutant=Indices_table["co"],cp=row["co"])
    if not math.isnan(co):
        num_count += 1
        p = max(p, co)
    so2 = row["so2"]
    # so2 = get_aqi_from_concentration(pollutant=Indices_table["so2"],cp=row["so2"])
    if not math.isnan(so2):
        num_count += 1
        p = max(p, so2)
    
    if num_count < 3 or (math.isnan(pm25) and math.isnan(pm10)):
        row["aqi"] = None
        row["aqi_bucket"] = None
    else:
        row["aqi"] = p
        aqi = Indices_table["AQI"]
        for k in range(0, len(Indices_table["AQI_Category"])):
            if(p >= aqi[k][0] and p <= aqi[k][1]):
                row["aqi_bucket"] = Buckets[k]
                break
    return row
