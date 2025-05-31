import sqlite3
import pandas as pd

def load_data_to_sqlite(csv_file='cleaned_aqi_data.csv', db_file='aqi_data.db'):
    # Load CSV into DataFrame
    df = pd.read_csv(csv_file)
    
    # Connect to SQLite database (creates file if not exists)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table with schema (if not exists)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aqi_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            aqi INTEGER,
            dominant_pollutant TEXT,
            time TEXT,
            pm25 REAL,
            pm10 REAL,
            o3 REAL,
            no2 REAL,
            co REAL,
            so2 REAL
        )
    ''')

    # Insert DataFrame into SQLite table
    df.to_sql('aqi_data', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()
    print(f"Data loaded successfully into {db_file}!")

if __name__ == "__main__":
    load_data_to_sqlite()
