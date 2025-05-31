from load_to_db import create_schema
create_schema()  # This will ensure tables are created before saving

import streamlit as st
import pandas as pd
import os
import sys
import plotly.express as px

# Add local directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fetch_data import fetch_aqi_data
from clean_data import clean_aqi_data
from load_to_db import save_data

# Set Streamlit config
st.set_page_config(page_title="🌍 Air Quality Dashboard", layout="wide")
st.title("🌬️ Air Quality ETL Dashboard")
st.markdown("Monitor, transform and analyze air pollution levels in real time.")

# --- Input widgets BEFORE fetching data ---
city = st.selectbox("🌆 Select City", ["paris", "london", "delhi", "beijing"])
token = st.text_input("🔐 Enter your AQICN API Token", type="password")

if city and token:
    with st.spinner("Fetching live data..."):
        raw_data = fetch_aqi_data(city, token)
        df = clean_aqi_data(raw_data)
        df = df.rename(columns={"datetime": "date"})
        # Rename 'pm2_5' to 'pm25' to match DB column
        df = df.rename(columns={"pm2_5": "pm25"})

        # Add synthetic AQI: simple average of pm10 and pm25
        df["aqi"] = df[["pm10", "pm25"]].mean(axis=1).astype(int)

        # Preview to confirm fix
        st.write("✅ Cleaned Data with AQI", df.head())

       
        st.write("📊 DataFrame Preview", df.head())
        st.write("📋 Columns in DF:", df.columns.tolist())

        save_data(df)

    # --- Continue with dashboard ---
    metric = st.selectbox("📊 Select Metric", ["pm10", "pm2_5", "co", "no2", "o3"])
    filtered = df  # Already filtered for 1 city
    filtered["date"] = pd.to_datetime(filtered["date"])
    fig1 = px.line(filtered, x="date", y=metric, title=f"{metric.upper()} Trend in {city}", color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📈 Correlation Heatmap")
    corr = filtered.select_dtypes(include='number').corr()
    fig2 = px.imshow(corr, text_auto=True, color_continuous_scale="Bluered")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📌 Quick Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average", f"{filtered[metric].mean():.2f}")
    col2.metric("Max", f"{filtered[metric].max():.2f}")
    col3.metric("Min", f"{filtered[metric].min():.2f}")
else:
    st.warning("Please select a city and enter your API token.")
