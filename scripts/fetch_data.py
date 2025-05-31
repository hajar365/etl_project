import requests

def fetch_aqi_data(city: str, token: str):
    """
    Fetch AQI data for a given city using the AQICN API.

    Args:
        city (str): City name (e.g., 'paris')
        token (str): Your AQICN API token

    Returns:
        dict: API response data (JSON)
    """
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            return data.get("data")
        else:
            raise Exception(f"API error: {data.get('data')}")
    else:
        raise Exception(f"HTTP error: {response.status_code}")
from fetch_data import fetch_aqi_data
def extract_relevant_data(raw_data):
    """
    Extract relevant fields from raw AQI API data.
    
    Args:
        raw_data (dict): Raw JSON response from API.
        
    Returns:
        dict: Cleaned data with key info.
    """
    data = {
        "city": raw_data.get("city", {}).get("name"),
        "aqi": raw_data.get("aqi"),
        "dominant_pollutant": raw_data.get("dominentpol"),
        "time": raw_data.get("time", {}).get("iso"),
        "pollutants": {}
    }
    
    pollutants = ["pm25", "pm10", "o3", "no2", "co", "so2"]
    iaqi = raw_data.get("iaqi", {})
    
    for p in pollutants:
        value = iaqi.get(p, {}).get("v")
        if value is not None:
            data["pollutants"][p] = value
    
    return data

API_TOKEN = "aebc8cacb02db2fade7aca7a0398f08950b656ef"
city = "paris"

data = fetch_aqi_data(city, API_TOKEN)
#print(data)
clean_data = extract_relevant_data(data)
print(clean_data)
import csv

def save_data_to_csv(data, filename="aqi_data.csv"):
    """
    Save a dictionary of AQI data to a CSV file.
    Args:
        data (dict): Cleaned AQI data
        filename (str): Output CSV file name
    """
    # Define CSV columns
    fields = ["city", "aqi", "dominant_pollutant", "time"] + list(data["pollutants"].keys())
    
    # Prepare one row for CSV
    row = {
        "city": data["city"],
        "aqi": data["aqi"],
        "dominant_pollutant": data["dominant_pollutant"],
        "time": data["time"],
    }
    # Add pollutant values
    for pollutant, value in data["pollutants"].items():
        row[pollutant] = value
    
    # Write to CSV
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)
    
    print(f"Data saved to {filename}")

# Example usage
if __name__ == "__main__":
    # Assuming 'data' is your cleaned data dict
    save_data_to_csv(clean_data)
def expand_data_with_forecast(raw_data):
    """
    From the raw API response, create multiple rows with daily forecast data.
    """
    base_info = {
        "city": raw_data.get("city", {}).get("name"),
        "dominant_pollutant": raw_data.get("dominentpol"),
    }
    time_info = raw_data.get("time", {}).get("iso")
    current_aqi = raw_data.get("aqi")

    daily_forecast = raw_data.get("forecast", {}).get("daily", {})
    pollutants = ["pm25", "pm10", "o3", "no2", "co", "so2"]

    rows = []

    # Loop over forecast days for pm25, for example
    pm25_forecast = daily_forecast.get("pm25", [])

    # We'll iterate over forecast days (assuming same days for each pollutant)
    for day_idx in range(len(pm25_forecast)):
        row = {
            "city": base_info["city"],
            "dominant_pollutant": base_info["dominant_pollutant"],
            "time": pm25_forecast[day_idx]["day"],
            "aqi": current_aqi,  # or you can leave blank or compute average
        }

        for p in pollutants:
            pollutant_forecast = daily_forecast.get(p, [])
            if pollutant_forecast and len(pollutant_forecast) > day_idx:
                row[p] = pollutant_forecast[day_idx]["avg"]
            else:
                row[p] = None

        rows.append(row)

    return rows
import requests
import csv
import random
from datetime import datetime, timedelta

API_TOKEN = "aebc8cacb02db2fade7aca7a0398f08950b656ef"
CITIES = ["paris", "london", "berlin", "madrid", "rome", "vienna", "amsterdam"]


def fetch_aqi_data(city: str, token: str):
    url = f"https://api.waqi.info/feed/{city}/?token={token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            return data.get("data")
        else:
            raise Exception(f"API error: {data.get('data')}")
    else:
        raise Exception(f"HTTP error: {response.status_code}")


def expand_data_with_forecast(raw_data):
    base_info = {
        "city": raw_data.get("city", {}).get("name"),
        "dominant_pollutant": raw_data.get("dominentpol"),
    }
    current_aqi = raw_data.get("aqi")
    daily_forecast = raw_data.get("forecast", {}).get("daily", {})
    pollutants = ["pm25", "pm10", "o3", "no2", "co", "so2"]
    rows = []

    pm25_forecast = daily_forecast.get("pm25", [])
    for day_idx in range(len(pm25_forecast)):
        row = {
            "city": base_info["city"],
            "dominant_pollutant": base_info["dominant_pollutant"],
            "time": pm25_forecast[day_idx]["day"],
            "aqi": current_aqi,
        }
        for p in pollutants:
            pollutant_forecast = daily_forecast.get(p, [])
            if pollutant_forecast and len(pollutant_forecast) > day_idx:
                row[p] = pollutant_forecast[day_idx]["avg"]
            else:
                row[p] = None
        rows.append(row)
    return rows


def vary_data(row, day_offset):
    new_row = row.copy()
    try:
        dt = datetime.strptime(new_row["time"], "%Y-%m-%d")
        dt += timedelta(days=day_offset)
        new_row["time"] = dt.strftime("%Y-%m-%d")
    except:
        pass

    for p in ["pm25", "pm10", "o3", "no2", "co", "so2"]:
        if new_row[p] is not None:
            variation = random.uniform(-0.1, 0.1)
            new_row[p] = round(new_row[p] * (1 + variation), 2)

    if new_row["aqi"] is not None:
        new_row["aqi"] = max(0, int(new_row["aqi"] * random.uniform(0.95, 1.05)))

    return new_row


def save_data_to_csv(rows, filename="aqi_data.csv"):
    fields = ["city", "aqi", "dominant_pollutant", "time", "pm25", "pm10", "o3", "no2", "co", "so2"]
    with open(filename, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to {filename}")


if __name__ == "__main__":
    collected_rows = []
    for city in CITIES:
        try:
            raw_data = fetch_aqi_data(city, API_TOKEN)
            forecast_rows = expand_data_with_forecast(raw_data)
            collected_rows.extend(forecast_rows)
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")

    # Now vary data to reach ~200 rows
    final_rows = []
    while len(final_rows) < 200:
        for idx, row in enumerate(collected_rows):
            varied_row = vary_data(row, idx)
            final_rows.append(varied_row)
            if len(final_rows) >= 200:
                break

    save_data_to_csv(final_rows)
