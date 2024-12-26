import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
from datetime import datetime
from datetime import timedelta

# API URL to fetch data
API_URL = "https://api.thingspeak.com/channels/1596152/feeds.json?results=100"

# Function to fetch data from the API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data['feeds']
    else:
        st.error("Failed to fetch data. Check your API key or network connection.")
        return None

# Function to calculate AQI based on pollutant values
def calculate_aqi(pm25, pm10, ozone, co):
    def aqi_sub_index(value, breakpoints):
        for bp in breakpoints:
            if bp[0] <= value <= bp[1]:
                return ((bp[3] - bp[2]) / (bp[1] - bp[0])) * (value - bp[0]) + bp[2]
        return None

    # Breakpoints for pollutants
    pm25_bp = [(0, 12, 0, 50), (12.1, 35.4, 51, 100), (35.5, 55.4, 101, 150), (55.5, 150.4, 151, 200), (150.5, 250.4, 201, 300), (250.5, 350.4, 301, 400), (350.5, 500.4, 401, 500)]
    pm10_bp = [(0, 54, 0, 50), (55, 154, 51, 100), (155, 254, 101, 150), (255, 354, 151, 200), (355, 424, 201, 300), (425, 504, 301, 400), (505, 604, 401, 500)]
    ozone_bp = [(0, 0.054, 0, 50), (0.055, 0.070, 51, 100), (0.071, 0.085, 101, 150), (0.086, 0.105, 151, 200), (0.106, 0.200, 201, 300)]
    co_bp = [(0, 4.4, 0, 50), (4.5, 9.4, 51, 100), (9.5, 12.4, 101, 150), (12.5, 15.4, 151, 200), (15.5, 30.4, 201, 300)]

    aqi_pm25 = aqi_sub_index(pm25, pm25_bp) or 0
    aqi_pm10 = aqi_sub_index(pm10, pm10_bp) or 0
    aqi_ozone = aqi_sub_index(ozone, ozone_bp) or 0
    aqi_co = aqi_sub_index(co, co_bp) or 0

    return max(aqi_pm25, aqi_pm10, aqi_ozone, aqi_co)

# Streamlit UI
st.title("Air Quality Monitoring🌏......!")

st.sidebar.subheader("Location📍")
city = st.sidebar.text_input("City")
state = st.sidebar.text_input("State")
country = st.sidebar.text_input("Country")
st.sidebar.write(f"Location: {city}, {state}, {country}")

# Date selection
st.sidebar.subheader("Select Date Range📅")
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=7))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Fields selection
st.sidebar.subheader("Select Fields to Display🧪 ")
fields = st.sidebar.multiselect(
    "Choose pollutants to display", 
    ["PM2.5", "PM10", "Ozone", "CO", "Temperature", "Humidity"], 
    default=["PM2.5", "PM10", "Ozone", "CO"]
)

# Fetch and display data based on the date range
if st.button("Fetch Air Quality Data🚀"):
    data = fetch_data()
    if data:
        st.success("Data fetched successfully✅!")

        # Filter data based on the selected date range
        filtered_data = []
        for entry in data:
            timestamp = datetime.strptime(entry['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            if start_date <= timestamp.date() <= end_date:
                filtered_data.append(entry)

        # Extract pollutant values from the filtered data
        pm25_values = [float(entry['field1']) if entry['field1'] else 0 for entry in filtered_data]
        pm10_values = [float(entry['field2']) if entry['field2'] else 0 for entry in filtered_data]
        ozone_values = [float(entry['field3']) if entry['field3'] else 0 for entry in filtered_data]
        humidity_values = [float(entry['field4']) if entry['field4'] else 0 for entry in filtered_data]
        temp_values = [float(entry['field5']) if entry['field5'] else 0 for entry in filtered_data]
        co_values = [float(entry['field6']) if entry['field6'] else 0 for entry in filtered_data]

        # Display all raw values
        st.subheader("Raw Pollutant Data📋")
        raw_data = pd.DataFrame(
            {
                "Timestamp": [entry['created_at'] for entry in filtered_data],
                "PM2.5": pm25_values,
                "PM10": pm10_values,
                "Ozone": ozone_values,
                "CO": co_values,
                "Humidity": humidity_values,
                "Temperature": temp_values
            }
        )
        st.dataframe(raw_data)

        # Calculate average pollutant values
        avg_pm25 = np.mean(pm25_values)
        avg_pm10 = np.mean(pm10_values)
        avg_ozone = np.mean(ozone_values)
        avg_co = np.mean(co_values)
        aqi = calculate_aqi(avg_pm25, avg_pm10, avg_ozone, avg_co)

        # Display AQI
        st.subheader(f"Calculated AQI: {aqi:.2f}")

        # Display pollutant levels in a table
        st.subheader("Average Pollutant Levels📊")
        pollutants = pd.DataFrame(
            {
                "Pollutant": ["PM2.5", "PM10", "Ozone", "CO", "Humidity", "Temperature"],
                "Average Value": [
                    avg_pm25 if "PM2.5" in fields else None,
                    avg_pm10 if "PM10" in fields else None,
                    avg_ozone if "Ozone" in fields else None,
                    avg_co if "CO" in fields else None,
                    np.mean(humidity_values) if "Humidity" in fields else None,
                    np.mean(temp_values) if "Temperature" in fields else None
                ],
            }
        )
        pollutants = pollutants.dropna(subset=["Average Value"])  # Drop rows with None
        st.table(pollutants)

        # Plot pollutant trends using Plotly (with field selection)
        st.subheader("Pollutant Trends")
        time_stamps = [datetime.strptime(entry['created_at'], "%Y-%m-%dT%H:%M:%SZ") for entry in filtered_data]

        fig = go.Figure()

        if "PM2.5" in fields:
            fig.add_trace(go.Scatter(x=time_stamps, y=pm25_values, mode='lines+markers', name='PM2.5', line=dict(color='blue')))
        if "PM10" in fields:
            fig.add_trace(go.Scatter(x=time_stamps, y=pm10_values, mode='lines+markers', name='PM10', line=dict(color='green')))
        if "Ozone" in fields:
            fig.add_trace(go.Scatter(x=time_stamps, y=ozone_values, mode='lines+markers', name='Ozone', line=dict(color='red')))
        if "CO" in fields:
            fig.add_trace(go.Scatter(x=time_stamps, y=co_values, mode='lines+markers', name='CO', line=dict(color='orange')))

        fig.update_layout(
            title="Pollutant Trends Over Time",
            xaxis_title="Time",
            yaxis_title="Concentration",
            legend_title="Pollutants",
            template="plotly_dark"
        )
        st.plotly_chart(fig)

        # Plot pollutant values using Matplotlib (with field selection)
        st.subheader("Environmental Measurements")
        fig, ax1 = plt.subplots(figsize=(12, 6))

        if "PM2.5" in fields:
            ax1.plot(pm25_values, label="PM2.5", color='b')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('PM2.5 (µg/m³)', color='b')
            ax1.tick_params(axis='y', labelcolor='b')

        if "PM10" in fields:
            ax1.plot(pm10_values, label="PM10", color='g')

        if "Ozone" in fields:
            ax1.plot(ozone_values, label="Ozone", color='r')

        if "Humidity" in fields:
            ax1.plot(humidity_values, label="Humidity", color='c')

        if "Temperature" in fields:
            ax1.plot(temp_values, label="Temperature", color='m')

        if "CO" in fields:
            ax1.plot(co_values, label="CO", color='y')

        ax1.legend()
        st.pyplot(fig)

        # Health recommendations based on AQI
        st.subheader("Health Recommendations")
        if aqi <= 50:
            st.markdown("- 🚨Air quality is considered satisfactory, and air pollution poses little or no risk.")
        elif aqi <= 100:
            st.markdown("- 🚨Air quality is acceptable; however, some pollutants may be a concern for sensitive groups.")
        elif aqi <= 150:
            st.markdown("- 🚨Members of sensitive groups may experience health effects; the general public is less likely to be affected.")
        elif aqi <= 200:
            st.markdown("- 🚨Health alert: everyone may experience health effects.")
        elif aqi <= 300:
            st.markdown("- 🚨Health warning of emergency conditions: everyone may experience more serious health effects.")
        else:
            st.markdown("- 🚨Hazardous: health alert, everyone may experience serious effects.")
