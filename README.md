Air Quality Monitoring Dashboard 🌍
This project is an interactive Air Quality Monitoring Dashboard built using Streamlit and Plotly. It allows users to visualize real-time air quality data fetched from the ThingSpeak API, including pollutant levels (PM2.5, PM10, Ozone, CO), temperature, and humidity. The dashboard provides detailed insights into air quality trends, calculated AQI (Air Quality Index), and health recommendations based on AQI levels.

Features:
Real-time Data Fetching: Fetch air quality data from ThingSpeak API.
Pollutant Trends: Visualize trends for PM2.5, PM10, Ozone, CO, and other air quality indicators over time.
Health Alerts: Get health alerts based on calculated AQI values.
Location-Based Data: Input city, state, and country to filter data specific to your location.
Customizable Filters: Select specific pollutants and filter data by date.
Interactive Visualizations: Interactive line charts for pollutant trends and a table showing average values of key pollutants.

Health Alerts:

🟢 Satisfactory: Air quality is good, poses little to no risk.
🟡 Moderate: Acceptable, but may concern sensitive individuals.
🟠 Unhealthy for Sensitive Groups: Health effects may occur for sensitive groups.
🔴 Unhealthy: Everyone may experience health effects.
🟣 Very Unhealthy: Health warning of emergency conditions.
⚫ Hazardous: Serious health effects for all.

Technologies Used:
Python
Streamlit: For building the web app.
Plotly: For creating interactive plots and visualizations.
Requests: For fetching data from the ThingSpeak API.
Pandas: For data manipulation and analysis.
Numpy: For numerical operations.

How to Use:
Clone or download this repository.
Install required dependencies: pip install -r requirements.txt.
Run the Streamlit app: streamlit run app.py.
Enter your desired location (City, State, Country) to fetch air quality data.
View pollutant trends, AQI values, and health alerts based on the data.

Installation:
Clone this repository to your local machine:
git clone https://github.com/your-username/air-quality-dashboard.git
Install the dependencies:
pip install -r requirements.txt
Run the app:
streamlit run app.py
