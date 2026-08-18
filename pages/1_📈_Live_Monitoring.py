# Import Library
import streamlit as st
from utils.influx_connection import get_latest_sensor_data

# Page Configuration
st.set_page_config(
    page_title="Live Monitoring",
    page_icon="📈",
    layout="wide"
)

# Page Title
st.title("📈 Live Bearing Monitoring")

st.markdown(
"""
Real-time vibration monitoring dashboard powered by InfluxDB 3.
"""
)

st.divider()

# ---------------------------------------
# Read Latest Sensor Data from InfluxDB
# ---------------------------------------

latest = get_latest_sensor_data()

time = latest["Time"]
mean = latest["Mean"]
peak = latest["Peak"]
peak_to_peak = latest["Peak_to_Peak"]
rms = latest["RMS"]
std = latest["Std"]

label = "Latest Sample"
# Professional Measurement Section
st.header("📊 Latest Bearing Sensor Measurement")

col1, col2, col3 = st.columns(3)

with col1:
    st.write(f"**Label:** {label}")
    st.write(f"**Mean:** {mean:.6f}")
    st.write(f"**Time:** {time}")

with col2:
    st.write(f"**Peak:** {peak:.4f}")
    st.write(f"**Peak-to-Peak:** {peak_to_peak:.4f}")

with col3:
    st.write(f"**RMS:** {rms:.4f}")
    st.write(f"**Std:** {std:.4f}")

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)