import sqlite3

def create_schema(db_path="aqi_data.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables
    c.execute('''
    CREATE TABLE IF NOT EXISTS Suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        country TEXT
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        supplier_id INTEGER,
        FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS EnvMetrics (
        metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        date TEXT,
        aqi INTEGER,
        pm25 REAL,
        pm10 REAL,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Schema created successfully.")

if __name__ == "__main__":
    create_schema()
import sqlite3
import pandas as pd

def save_data(df: pd.DataFrame, db_path="aqi_data.db", product_id=1):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for _, row in df.iterrows():
        c.execute('''
            INSERT INTO EnvMetrics (product_id, date, aqi, pm25, pm10)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            product_id,
            row["date"],
            row["aqi"],
            row["pm25"],
            row["pm10"]
        ))

    conn.commit()
    conn.close()
    print("Cleaned data saved to EnvMetrics table.")
