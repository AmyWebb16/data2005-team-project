
import pandas as pd
import numpy as np
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAGE 3: ANALYSIS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~

os.makedirs("reports", exist_ok=True)
log_file = open("outputs/reports/analysis_output.txt", "w")

def log(msg=""):
    print(msg)           
    log_file.write(str(msg) + "\n")

df = pd.read_csv("data/processed/processed_data.csv", parse_dates=["date"])
log("\ndata loaded")

# Device rename
DEVICES = sorted(df["device"].unique())

DEVICE_LABELS = {
    DEVICES[0]: "Sensor A",
    DEVICES[1]: "Sensor B",
    DEVICES[2]: "Sensor C",
}

df["device"] = df["device"].replace(DEVICE_LABELS)

# ---- descriptive stats ----
def descriptive_stats(df):
    """sum stats for all num sensor columns"""
    sensor_cols = ["temp", "humidity", "co", "lpg", "smoke", "total_gas"]

    stats_by_device = {}
    for device, group in df.groupby("device"):
        arr = group[sensor_cols].to_numpy()
        stats = pd.DataFrame({
            "mean":   np.mean(arr, axis=0),
            "median": np.median(arr, axis=0),
            "std":    np.std(arr, axis=0, ddof=1),
            "min":    np.min(arr, axis=0),
            "max":    np.max(arr, axis=0),
        }, index=sensor_cols)
        stats_by_device[device] = stats

        log(f"\n---- Descriptive Statistics, Device: {device} ----")
        log(stats.round(4))

    return stats_by_device


# ---- Thermal Comfort Index ----
def thermal_comfort_index(df):
    """Calculate Thermal Comfort Index """
    df = df.copy()
    RH = df["humidity"].to_numpy()
    if RH.max() <= 1.0:
        RH = RH * 100.0
    T = df["temp"].to_numpy()

    df["tci"]     = (T - (0.55 - 0.0055 * RH) * (T - 14.5)).round(2)
    df["comfort"] = np.where(df["tci"] < 21, "Comfortable", "Uncomfortable")

    log("\n---- Thermal Comfort Index ----")
    comfort_by_device = (
        df.groupby(["device", "comfort"])
          .size()
          .unstack(fill_value=0)
    )
    log(comfort_by_device)
    return df[["device", "tci", "comfort"]]


# ---- anomaly detection ----
def detect_anomalies(df, threshold=3.0):

    sensor_cols = ["co", "humidity", "lpg", "smoke", "temp", "total_gas"]
    all_anomalies = []

    log(f"\n---- Anomaly Detection ----")

    for device, group in df.groupby("device"):

        # Step 1: Calculate the mean and std for each sensor
        mean = stats[device]["mean"]
        std  = stats[device]["std"]

        # how far each reading is from the avg
        z_scores = (group[sensor_cols] - mean) / std

        is_anomaly = z_scores.abs().max(axis=1) > threshold

        anomaly_df = group[is_anomaly]
        all_anomalies.append(anomaly_df)
        
        rate = len(anomaly_df) / len(group) * 100
        log(f"  {device}: {len(anomaly_df)} anomalies / {len(group)} readings ({rate:.2f}%)")

    return pd.concat(all_anomalies)


# ---- usage patterns ----
def usage_patterns(df):
    """sensor avgs and occupancy by weekday"""

    by_device = (
        df.groupby("device")[["temp", "humidity", "co", "total_gas"]]
          .mean()
    )
    log("\n---- Average Readings ----")
    log(by_device.round(4))

    weekday_order = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]
    df = df.copy()
    df["weekday"] = pd.Categorical(df["weekday"], categories=weekday_order, ordered=True)

    by_weekday_device = (
        df.groupby(["device", "weekday"], observed=True)["temp"]
          .mean()
          .unstack(level=0)
    )
    log("\n---- Average Temperature by weekday ----")
    log(by_weekday_device.round(4))

    occupancy = (
        df.groupby("device")["motion"]
          .mean()
          .rename("occupancy_rate")
          .to_frame()
    )
    log("\n---- Occupancy Rate ----")
    log(occupancy.round(4))

    return by_device, by_weekday_device, occupancy


# ---- correlation analysis ----
def correlation_analysis(df):
    """correlation matrix"""
    sensor_cols = ["temp", "humidity", "co", "lpg", "smoke", "total_gas"]

    corr_by_device = {}
    for device, group in df.groupby("device"):
        arr      = group[sensor_cols].to_numpy().T
        corr_mat = np.corrcoef(arr)
        corr_df  = pd.DataFrame(corr_mat, index=sensor_cols, columns=sensor_cols)
        corr_by_device[device] = corr_df

        log(f"\n---- Correlation Matrix, Device: {device} ----")
        log(corr_df.round(3))

    return corr_by_device

# ---- run analysis ----

if __name__ == "__main__":
    stats     = descriptive_stats(df)
    comfort   = thermal_comfort_index(df)
    anomalies = detect_anomalies(df)
    patterns  = usage_patterns(df)
    corr      = correlation_analysis(df)
    
    # ---- save outputs for visualisation ----
    average_readings, avg_temp_weekday, occupancy = patterns

    df.to_csv("data/processed/cleaned_df.csv", index=False)                        
    comfort.to_csv("data/processed/comfort.csv", index=False)                      
    anomalies.to_csv("data/processed/anomalies.csv", index=False)                  
    average_readings.to_csv("data/processed/avg_readings.csv")                            
    avg_temp_weekday.to_csv("data/processed/avg_temp_weekday.csv")                
    occupancy.to_csv("data/processed/occupancy.csv")                               

    log("\n all outputs saved")