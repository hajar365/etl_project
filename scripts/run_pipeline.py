from fetch_data import fetch_aqi_data, expand_data_with_forecast, vary_data, save_data_to_csv

API_TOKEN = "aebc8cacb02db2fade7aca7a0398f08950b656ef"
CITIES = ["paris", "london", "berlin", "madrid", "rome", "vienna", "amsterdam"]

def run_etl_pipeline():
    collected_rows = []

    for city in CITIES:
        try:
            raw_data = fetch_aqi_data(city, API_TOKEN)
            forecast_rows = expand_data_with_forecast(raw_data)
            collected_rows.extend(forecast_rows)
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")

    final_rows = []
    while len(final_rows) < 200:
        for idx, row in enumerate(collected_rows):
            varied_row = vary_data(row, idx)
            final_rows.append(varied_row)
            if len(final_rows) >= 200:
                break

    save_data_to_csv(final_rows, filename="aqi_data.csv")

if __name__ == "__main__":
    run_etl_pipeline()
