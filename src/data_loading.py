import pandas as pd


# ~~~~~~~~~~~~~~~~~~~~~~~
# STAGE 1: DATA INGESTION
# ~~~~~~~~~~~~~~~~~~~~~~~


def validate_cols(df):
    """
    Check if all required columns exist in DataFrame
    """

    # ===== Validate required columns exist =====
    required_cols = ["ts", "device", "co", "humidity", "light", "lpg", "motion", "smoke", "temp"]
    missing_col = []
    missing_num = 0

    # Check if columns exist
    for col in required_cols:
        if col not in df.columns:
            missing_col.append(col)
            missing_num += 1
    
    # No missing columns
    if missing_num == 0:
        return True
    else:
        # Display missing column(s) error
        raise KeyError ("Missing required Column(s)", missing_col)



def load_raw_dataset():
    """
    Load data into DataFrame
    """

    try:
        # ===== Load raw IoT dataset =====
        df = pd.read_csv("data/raw/iot_telemetry_data.csv")

        # Check if required columns exist
        if validate_cols(df) == True:
            print("\nData is loaded successfully.\n")
            return df

    # ===== Handle file not found error =====
    except FileNotFoundError:
        raise FileNotFoundError ("File not found. Check if the file path is correct.")
    
if __name__ == "__main__":
    df = load_raw_dataset()
    df.info()