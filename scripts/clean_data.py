import pandas as pd
from datetime import datetime

def clean_aqi_data(data_dict):
    """
    Cleans AQI JSON data and returns a DataFrame.
    Args:
        data_dict (dict): JSON data from the AQICN API.
    Returns:
        pd.DataFrame: Cleaned and structured AQI data.
    """

    # Check if 'forecast' and 'daily' are in data
    if 'forecast' not in data_dict or 'daily' not in data_dict['forecast']:
        raise ValueError("Missing 'forecast.daily' data in API response.")

    daily = data_dict["forecast"]["daily"]
    city = data_dict["city"]["name"]

    records = []

    for metric, values in daily.items():
        for entry in values:
            records.append({
                "city": city,
                "datetime": entry.get("day"),
                "metric": metric,
                "value": entry.get("avg")
            })

    df = pd.DataFrame(records)

    # Pivot to have one row per datetime with metrics as columns
    df = df.pivot(index=["datetime", "city"], columns="metric", values="value").reset_index()

    # Rename columns (optional)
    df.columns.name = None
    df.rename(columns={"pm25": "pm2_5"}, inplace=True)

    return df