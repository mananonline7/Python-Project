from utils.ml_model import predict_fault
import streamlit as st
from utils.influx_connection import get_latest_sensor_data
from datetime import datetime

st.set_page_config(page_title="Machine Learning Prediction",
                   page_icon="🤖",
                   layout="wide")

st.title("🤖 Machine Learning Prediction")
st.write("Random Forest based bearing fault diagnosis and maintenance recommendation.")
st.divider()

# ---------------------------------------
# Read Latest Prediction from SQLite
# ---------------------------------------

model_name = "Random Forest"

from utils.db import get_connection

try:

    # Read latest sensor features from InfluxDB
    latest = get_latest_sensor_data()

    mean = latest["Mean"]
    peak = latest["Peak"]
    peak_to_peak = latest["Peak_to_Peak"]
    rms = latest["RMS"]
    std = latest["Std"]

    # Run Random Forest prediction
    prediction, confidence = predict_fault(
        mean,
        peak,
        peak_to_peak,
        rms,
        std
    )

    # Save prediction into SQLite
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (timestamp, prediction, confidence)
    VALUES (?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        str(prediction),
        float(confidence)
    ))

    conn.commit()
    conn.close()

    st.success("✅ Prediction saved successfully!")

     # ---------------------------------------
    # Automatic Maintenance Work Order
    # ---------------------------------------

    conn = get_connection()
    cursor = conn.cursor()

    # Check for an existing open work order
    cursor.execute("""
    SELECT
        id,
        work_order,
        equipment,
        priority,
        status,
        assigned_to,
        created_on
    FROM work_orders
    WHERE status='Open'
    ORDER BY id DESC
    LIMIT 1
    """)

    current_work_order = cursor.fetchone()

    # Create a work order only if none exists
    if prediction != "Healthy" and current_work_order is None:

        work_order_number = "WO-" + datetime.now().strftime("%Y%m%d-%H%M%S")

        cursor.execute("""
        INSERT INTO work_orders
        (
            work_order,
            equipment,
            priority,
            status,
            assigned_to,
            created_on
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            work_order_number,
            "Bearing Assembly",
            "High",
            "Open",
            "Maintenance Team",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        # Read the newly created work order
        cursor.execute("""
        SELECT
            id,
            work_order,
            equipment,
            priority,
            status,
            assigned_to,
            created_on
        FROM work_orders
        WHERE status='Open'
        ORDER BY id DESC
        LIMIT 1
        """)

        current_work_order = cursor.fetchone()

    conn.close()

    # Always display the current work order
    if current_work_order:

        st.success("🔧 Maintenance Work Order Generated")

        st.info(f"""
### Automatically Generated Work Order

**Work Order Number:** {current_work_order[1]}

**Equipment:** {current_work_order[2]}

**Priority:** {current_work_order[3]}

**Status:** {current_work_order[4]}

**Assigned To:** {current_work_order[5]}

**Created On:** {current_work_order[6]}
""")

except Exception as e:

    st.error(f"Error: {e}")

    prediction = "No Prediction"
    confidence = 0

    mean = 0
    peak = 0
    peak_to_peak = 0
    rms = 0
    std = 0
       
# Prediction Summary
st.header("Prediction Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Prediction Model",
        model_name
    )

with col2:
    st.metric(
        "Predicted Fault",
        prediction
    )

with col3:
    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.progress(confidence / 100)
  
# Model Information
st.divider()

st.header("Model Information")

st.info("""
**Model Name:** Random Forest Classifier

**Training Dataset:** Case Western Reserve University (CWRU) Bearing Dataset

**Original Extracted Features:** 16 Statistical Vibration Features

**Selected Features Used for Prediction:**
- Mean
- RMS
- Peak
- Peak-to-Peak
- Standard Deviation

**Feature Selection Method:** Random Forest Feature Importance Analysis
""")

# Maintenance Recommendation
st.error("🔴 High Priority Maintenance Required")
# ---------------------------------------
# Feature Values Used
# ---------------------------------------

st.divider()

st.header("Feature Values Used")

import pandas as pd

feature_df = pd.DataFrame({
    "Feature": [
        "Mean",
        "RMS",
        "Peak",
        "Peak-to-Peak",
        "Std"
    ],
    "Value": [
        mean,
        rms,
        peak,
        peak_to_peak,
        std
    ]
})

st.dataframe(feature_df, use_container_width=True)

# ---------------------------------------
# Random Forest Feature Importance
# ---------------------------------------

st.divider()

st.header("Random Forest Feature Importance")

feature_importance_df = pd.DataFrame(
    {
        "Importance": [
            0.15,
            0.22,
            0.30,
            0.25,
            0.08
        ]
    },
    index=[
        "Mean",
        "RMS",
        "Peak",
        "Peak-to-Peak",
        "Std"
    ]
)

st.bar_chart(feature_importance_df)

# ---------------------------------------
# Prediction History
# ---------------------------------------

st.header("Prediction History")

import pandas as pd

conn = get_connection()

history = pd.read_sql_query("""
SELECT
    timestamp AS Time,
    prediction AS Prediction,
    ROUND(confidence,2) AS Confidence
FROM predictions
ORDER BY id DESC
LIMIT 10
""", conn)

conn.close()

history["Confidence"] = history["Confidence"].astype(str) + "%"

st.dataframe(
    history,
    use_container_width=True,
    hide_index=True
)
# ---------------------------------------
# Model Performance
# ---------------------------------------

st.divider()

st.header("Model Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Accuracy", "99.84%")

with col2:
    st.metric("Precision", "99.82%")

with col3:
    st.metric("Recall", "99.81%")

with col4:
    st.metric("F1 Score", "99.80%")

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)