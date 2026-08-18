import os
from pathlib import Path

import pandas as pd
import streamlit as st
from influxdb_client_3 import InfluxDBClient3

CSV_FALLBACK_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset_from_influxdb.csv"

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
# Tries live InfluxDB first (for local/real deployments). If InfluxDB is
# unreachable — e.g. this app is hosted online with no public InfluxDB
# server configured — falls back to the latest row of the bundled dataset
# export so the page still has something real to show.

def _get_latest_from_influxdb():

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
        "Time": latest["time"],
        "Source": "InfluxDB (live)"
    }


def _get_latest_from_csv():

    df = pd.read_csv(CSV_FALLBACK_PATH)

    latest = df.sort_values("time").iloc[-1]

    return {
        "Mean": latest["Mean"],
        "Peak": latest["Peak"],
        "Peak_to_Peak": latest["Peak_to_Peak"],
        "RMS": latest["RMS"],
        "Std": latest["Std"],
        "Label": latest["Label"],
        "Time": latest["time"],
        "Source": "Dataset snapshot (InfluxDB unavailable)"
    }


def get_latest_sensor_data():

    try:
        return _get_latest_from_influxdb()
    except Exception:
        return _get_latest_from_csv()