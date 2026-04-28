from data_loading import load_raw_dataset
import pandas as pd


# ~~~~~~~~~~~~~~~~~~~~~~
# STAGE 2: DATA CLEANING
# ~~~~~~~~~~~~~~~~~~~~~~

# ===== Load data =====
df = load_raw_dataset()


# ===== Remove duplicate timestamp and device combinations =====
duplicated_rows = df.duplicated(subset=["ts", "device"]).sum()

if duplicated_rows != 0:
    df = df.drop_duplicates(subset=['ts', 'device'])
    
    print(f"\nDuplicated rows: {duplicated_rows}")
    print("All duplicated rows are removed")
else:
    print("\nNo duplicated rows")


# ===== Check missing values =====
missing_val = df.isna().sum()
if missing_val.all() == 0:
    print("\nNo missing values")
else:
    print(missing_val)


# ===== Remove outliers =====
def remove_outliers(col):
    """
    Remove outliers values
    """

    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3-q1
    lower = q1 - iqr * 1.5
    upper = q3 + iqr * 1.5

    # get values within max and min
    non_outliers = (df[col] >= lower) & (df[col] <= upper)
    return df[non_outliers]

# get numeric columns
numeric_cols = df.select_dtypes(include='number').columns[1:]
for col in numeric_cols:
    df = remove_outliers(col)

print("\nOutliers are removed")


# ===== Convert data types =====
# convert ts into datetime
df['datetime'] = pd.to_datetime(df['ts'], unit='s', utc=True)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STAGE 3: DATA TRANSFORMATION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ===== Extract temporal features (day, time, weekday) =====
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time
df['weekday'] = df['datetime'].dt.day_name()


# ===== Calculate derived columns =====
df['total_gas'] = df['co'] + df['lpg'] + df['smoke']


# ===== Reorder Dataframe columns =====
# remove original timestamp ('ts')
df = df.drop(columns=['ts', 'datetime'])

# move columne datatime to front
move_cols = ['date', 'time', 'weekday']
df = df[move_cols + [col for col in df.columns if col not in move_cols]]

print("\nNew column structure:")
df.info()


# ~~~~~~~~~~~~~~~~~~~~~~~~~
# STAGE 4: DATA EXPORTATION 
# ~~~~~~~~~~~~~~~~~~~~~~~~~

df.to_csv("data/processed/processed_data.csv", index=False)
print("\nProcessed data is saved in data/processed/processed_data.csv")