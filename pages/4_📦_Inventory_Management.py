# Imports
import streamlit as st
import pandas as pd

from utils.db import get_connection

# Page Configuration
st.set_page_config(
    page_title="Inventory Management",
    page_icon="📦",
    layout="wide"
)

# Page Header
st.title("📦 Inventory Management")

st.write(
    "Monitor spare bearing availability and inventory levels for predictive maintenance."
)

st.divider()

# ---------------------------------------
# Read Inventory from SQLite
# ---------------------------------------

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
SELECT
bearing,
stock,
minimum_stock,
supplier,
location,
lead_time
FROM inventory
ORDER BY id DESC
LIMIT 1
""")

row = cursor.fetchone()

conn.close()

# ---------------------------------------
# Read Latest Prediction
# ---------------------------------------

conn = get_connection()
cursor = conn.cursor()

cursor.execute("""
SELECT prediction
FROM predictions
ORDER BY id DESC
LIMIT 1
""")

prediction_row = cursor.fetchone()

conn.close()

if prediction_row:
    predicted_fault = prediction_row[0]
else:
    predicted_fault = "Healthy"

if row:

    bearing = row[0]
    stock = row[1]
    minimum = row[2]
    supplier = row[3]
    location = row[4]
    lead_time = row[5]

else:

    bearing = "No Data"
    stock = 0
    minimum = 0
    supplier = "-"
    location = "-"
    lead_time = "-"

# Inventory Summary
st.header("Inventory Summary")

st.header("Machine Learning Spare Part Recommendation")

st.metric(
    "Predicted Fault",
    predicted_fault
)

if predicted_fault == "Healthy":

    st.success("✅ No spare part is required.")

else:

    st.info(f"""
### Recommended Spare Part

Bearing Type : 6205 Bearing

Detected Fault : Outer Race Fault

Recommended Action : Replace Bearing Immediately

Required Quantity : 1 Unit

machine learning prediction detected:

**{predicted_fault}**
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Bearing", bearing)

with col2:
    st.metric("Available Stock", stock)

with col3:
    st.metric("Minimum Stock", minimum)

# Additional Information
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write("### Supplier")
    st.write(supplier)

with col2:
    st.write("### Warehouse Location")
    st.write(location)
  
# Lead Time
st.divider()

st.subheader("Delivery Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Supplier**")
    st.write(supplier)

    st.write("**Lead Time**")
    st.write(lead_time)

with col2:
    st.write("**Warehouse**")
    st.write(location)

# Stock Status
st.divider()

st.header("Inventory Status")

# Status Logic
if stock >= minimum + 2:
    st.success("✅ Spare Bearing Available (Stock: 8 Units)")

elif stock > minimum:
    st.warning("🟡 Stock is above minimum, but replenishment is recommended.")

elif stock == minimum:
    st.warning("🟠 Minimum Stock Level Reached")

else:
    st.error("🔴 Stock Below Minimum Level – Purchase Required")

# Inventory Table

st.divider()

st.header("Current Spare Parts Inventory")

inventory_df = pd.DataFrame({

    "Bearing":[bearing],

    "Stock":[stock],

    "Minimum Stock":[minimum],

    "Supplier":[supplier],

    "Location":[location],

    "Lead Time":[lead_time]

})

st.dataframe(
    inventory_df,
    use_container_width=True
)

# Inventory Recommendation
st.divider()

st.header("Recommendation")

if stock > minimum:

    st.info(
        "6205 Bearing is available in stock and maintenance can proceed immediately without procurement delay."
    )

elif stock == minimum:

    st.warning(
        "Reorder is recommended to avoid future shortages."
    )

else:

    st.error(
        "Immediate purchase order required."
    )

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)