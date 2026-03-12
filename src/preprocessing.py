from data_loading import load_data
import pandas as pd


# ~~~~~~~~~~~~~~~~~~~~~~
# STAGE 2: DATA CLEANING
# ~~~~~~~~~~~~~~~~~~~~~~

# ===== Load data =====
df = load_data()


# ===== Remove duplicate timestamp and device combinations =====
duplicated_rows = df.duplicated(subset=["ts", "device"]).sum()
if duplicated_rows != 0:
    print(f"\nDuplicated rows: {duplicated_rows}")
    df = df.drop_duplicates(subset=['ts', 'device'])
else:
    print("\nNo duplicated rows")


# ===== Check missing values =====
missing_val = df.isna().sum()
print(missing_val)

cols = df.select_dtypes(include='number').columns[1:]


# ===== Remove outliers =====
def remove_outliers(col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3-q1
    lower = q1 - iqr * 1.5
    upper = q3 + iqr * 1.5

    # get values within max and min
    non_outliers = (df[col] >= lower) & (df[col] <= upper)
    return df[non_outliers]
 
for col in cols:
    df = remove_outliers(col)


# ===== Convert data types =====
# convert ts into datetime
df['datetime'] = pd.to_datetime(df['ts'], unit='s', utc=True)

# move columne datatime next ts (timestamp)
col = df.pop('datetime')
df.insert(1, 'datetime', col)

print(df.head)