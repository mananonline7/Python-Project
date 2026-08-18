import os

import streamlit as st
from influxdb_client_3 import InfluxDBClient3

# -----------------------------------
# InfluxDB Configuration
# -----------------------------------
# Credentials are read from Streamlit secrets (.streamlit/secrets.toml,
# gitignored) or environment variables — never hardcode them here, since
# this file is committed to a public repo.


def _get_config(key, default=None):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key, default)


HOST = _get_config("INFLUXDB_HOST", "http://localhost:8181")

DATABASE = _get_config("INFLUXDB_DATABASE", "dissertation")

TOKEN = _get_config("INFLUXDB_TOKEN")

client = InfluxDBClient3(
    host=HOST,
    token=TOKEN,
    database=DATABASE
)


# -----------------------------------
# Get Latest Sensor Features
# -----------------------------------

def get_latest_sensor_data():

    query = """
    SELECT *
    FROM bearing_features
    ORDER BY time DESC
    LIMIT 1
    """

    table = client.query(query=query)

    df = table.to_pandas()

    latest = df.iloc[0]

    return {
        "Mean": latest["Mean"],
        "Peak": latest["Peak"],
        "Peak_to_Peak": latest["Peak_to_Peak"],
        "RMS": latest["RMS"],
        "Std": latest["Std"],
        "Label": latest["Label"],
        "Time": latest["time"]
    }