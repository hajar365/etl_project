import pandas as pd

def transform_aqi_data(input_file="cleaned_aqi_data.csv", output_file="transformed_aqi_data.csv"):
    df = pd.read_csv(input_file)

    # 1. Convert time to datetime (if not already)
    df["time"] = pd.to_datetime(df["time"])

    # 2. Add time-based features
    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["weekday"] = df["time"].dt.day_name()
    df["hour"] = df["time"].dt.hour

    # 3. Categorize AQI levels (based on EPA standards)
    def categorize_aqi(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    df["aqi_category"] = df["aqi"].apply(categorize_aqi)

    # 4. Normalize pollutant columns (Min-Max normalization)
    pollutant_cols = ["pm25", "pm10", "o3", "no2", "co", "so2"]
    for col in pollutant_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val - min_val != 0:
            df[f"{col}_norm"] = (df[col] - min_val) / (max_val - min_val)
        else:
            df[f"{col}_norm"] = 0  # if no variation

    # Save transformed data
    df.to_csv(output_file, index=False)
    print(f"[📊] Transformed data saved to {output_file} with {len(df)} rows.")

if __name__ == "__main__":
    transform_aqi_data()
