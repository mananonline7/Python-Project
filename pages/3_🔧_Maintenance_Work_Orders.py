from utils.db import get_connection

conn = get_connection()
cursor = conn.cursor()
# Imports
import streamlit as st
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Maintenance Work Orders",
    page_icon="🔧",
    layout="wide"
)

# Header
st.title("🔧 Maintenance Work Orders")

st.write(
    "Automatically generated maintenance work orders based on machine learning predictions."
)

#st.divider()

# Read latest prediction
cursor.execute("""
SELECT prediction,
       confidence,
       timestamp
FROM predictions
ORDER BY id DESC
LIMIT 1
""")

prediction, confidence, generated = cursor.fetchone()

# Read inventory
cursor.execute("""
SELECT bearing,
       stock,
       minimum_stock
FROM inventory
LIMIT 1
""")

equipment, stock, minimum_stock = cursor.fetchone()

# Read latest work order

cursor.execute("""
SELECT work_order,
       equipment,
       priority,
       status,
       assigned_to,
       created_on
FROM work_orders
ORDER BY id DESC
LIMIT 1
""")

work_order, equipment, priority, status, engineer, generated = cursor.fetchone()

if prediction == "Ball Fault":
    recommended_action = "Replace Bearing Immediately"

elif prediction == "Inner Race Fault":
    recommended_action = "Inspect Inner Race and Replace Bearing"

elif prediction == "Outer Race Fault":
    recommended_action = "Replace Bearing Immediately"

else:
    recommended_action = "Continue Normal Operation"

# Work Order Summary
st.divider()

st.header("Work Order Summary")

col1, col2 = st.columns(2)

with col1:

    st.write("**Work Order ID**")
    st.write(work_order)

    st.write("**Equipment**")
    st.write(equipment)

with col2:

    st.write("**Assigned Engineer**")
    st.write(engineer)

    st.write("**Generated On**")
    st.write(generated)
  
# Priority and Status
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.write("### Priority")
    st.write(priority)

with col2:
    st.write("### Status")
    st.write(status)

with col3:
    st.write("### ML Confidence")
    st.metric("Prediction", f"{confidence:.2f}%")
  
# Status Indicator
st.divider()

st.header("Current Status")
if prediction == "Healthy":
    st.success("✅ No Work Order Required")
else:
    st.error("🔴 High Priority Work Order Open ")

# Recommended Action
st.divider()

st.header("Maintenance Recommendation")

st.info(
    f"""
Recommended Action

{recommended_action}

Priority

{priority}
"""
)

# Maintenance Checklist
st.divider()

st.header("Maintenance Checklist")

if prediction != "Healthy":

    st.checkbox("Isolate Machine")
    st.checkbox("Lockout / Tagout")
    st.checkbox("Replace Bearing")
    st.checkbox("Inspect Shaft")
    st.checkbox("Install New Bearing")
    st.checkbox("Functional Test")
    st.checkbox("Close Work Order")

else:

    st.success("No maintenance activities required.")
# Work Order Information
st.divider()

st.header("Work Order Details")

st.write(f"""
This maintenance work order has been automatically generated
following a machine learning prediction.

Equipment:
**{equipment}**

Detected Fault:
**{prediction}**

Prediction Confidence:
**{confidence:.2f}%**

Recommended Action:
**{recommended_action}**

Priority:
**{priority}**
""")

# Close Connection
conn.close()

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)

