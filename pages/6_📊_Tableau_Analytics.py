import streamlit.components.v1 as components

from utils.db import get_connection

conn = get_connection()
cursor = conn.cursor()
# Import streamlit
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tableau Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# Read the latest prediction
# --------------------------------------------------
cursor.execute("""
SELECT bearing,
       stock,
       minimum_stock
FROM inventory
ORDER BY id DESC
LIMIT 1
""")

bearing, stock, minimum_stock = cursor.fetchone()

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("📊 Tableau Analytics")

st.write(
    "Executive dashboard for predictive maintenance performance and business analytics."
)

st.divider()

# --------------------------------------------------
# Read work order
# --------------------------------------------------
cursor.execute("""
SELECT work_order,
       status,
       priority
FROM work_orders
ORDER BY id DESC
LIMIT 1
""")

work_order, work_status, priority = cursor.fetchone()

# --------------------------------------------------
# KPI DASHBOARD
# --------------------------------------------------

st.header("Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

# Database Counts
cursor.execute("SELECT COUNT(*) FROM predictions")
prediction_count = cursor.fetchone()[0]

cursor.execute("""
SELECT COUNT(*)
FROM predictions
WHERE prediction != 'Healthy'
""")
fault_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM work_orders")
workorder_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM email_logs")
email_count = cursor.fetchone()[0]

# Latest Prediction
cursor.execute("""
SELECT prediction
FROM predictions
ORDER BY id DESC
LIMIT 1
""")
latest_prediction = cursor.fetchone()[0]

# Shorten display text
if latest_prediction == "Outer Race Fault":
    latest_prediction = "Outer Fault"


# Latest Inventory Stock
cursor.execute("""
SELECT stock
FROM inventory
ORDER BY id DESC
LIMIT 1
""")
stock = cursor.fetchone()[0]

# KPI Cards
with col1:
    st.metric(
        "Latest Prediction",
        latest_prediction
    )

with col2:
    st.metric(
        "Open Work Orders",
        workorder_count
    )

with col3:
    st.metric(
        "Spare Bearings",
        stock
    )

with col4:
    st.metric(
        "Email Notifications",
        email_count
    )

st.divider()
# --------------------------------------------------
# MACHINE HEALTH
# --------------------------------------------------

st.header("Machine Health Overview")

cursor.execute("""
SELECT prediction,
       confidence
FROM predictions
ORDER BY id DESC
LIMIT 1
""")

prediction, confidence = cursor.fetchone()

health_df = pd.DataFrame({
    "Machine": ["Bearing Test Rig"],
    "Condition": [prediction],
    "Confidence": [f"{confidence:.2f}%"]
})

st.dataframe(
    health_df,
    use_container_width=True
)
st.divider()

# --------------------------------------------------
# BUSINESS PERFORMANCE
# --------------------------------------------------

st.header("Business Performance")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Machine Availability",
        "98.5%"
    )

with c2:
    st.metric(
        "Downtime Avoided",
        "24 Hours"
    )

with c3:
    st.metric(
        "Maintenance Cost Saved",
        "€12,500"
    )

st.divider()

# --------------------------------------------------
# INVENTORY ANALYTICS
# --------------------------------------------------

st.header("Inventory Analytics")

inventory_df = pd.read_sql_query(
    """
    SELECT
        bearing,
        stock,
        minimum_stock,
        supplier,
        location,
        lead_time
    FROM inventory
    """,
    conn
)

st.dataframe(
    inventory_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# MAINTENANCE SUMMARY
# --------------------------------------------------

st.header("Maintenance Summary")

summary_df = pd.read_sql_query(
    """
    SELECT
        work_order,
        equipment,
        priority,
        status,
        assigned_to,
        created_on
    FROM work_orders
    """,
    conn
)

st.dataframe(
    summary_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# TABLEAU DASHBOARD
# --------------------------------------------------

st.header("📊 Interactive Tableau Dashboards")

tab1, tab2, tab3 = st.tabs([
    "CWRU Analytics",
    "Maintenance Dashboard",
    "InfluxDB Monitoring"
])

# CWRU Dash Board
with tab1:
    st.subheader("CWRU Predictive Maintenance Dashboard")

    st.info(
      "💡 Click **Open Full Interactive Dashboard** for the complete Tableau experience, including full-screen view, filters, and export options."
  )
  
    st.link_button(
      "🔗 Open Full Interactive Dashboard",
                                             "https://public.tableau.com/views/CWRU_Predictive_Maintenance_Dashboard/CWRUPredictiveMaintenanceSystem?:showVizHome=no"
)

    components.iframe(
        "https://public.tableau.com/views/CWRU_Predictive_Maintenance_Dashboard/CWRUPredictiveMaintenanceSystem?:showVizHome=no",
        height=1100,
        scrolling=True
    )
# Maintenance Dashboard
with tab2:
    st.subheader("Maintenance Operations Dashboard")

    st.info(
      "💡 Click **Open Full Interactive Dashboard** for the complete Tableau experience, including full-screen view, filters, and export options."
  )

    st.link_button(
        "🔗 Open Full Interactive Dashboard",
               "https://public.tableau.com/views/MaintenanceOperationsDashboard/MaintenanceOperationsDashboard?:showVizHome=no"
    )

    components.iframe(
        "https://public.tableau.com/views/MaintenanceOperationsDashboard/MaintenanceOperationsDashboard?:showVizHome=no",
        height=1100,
        scrolling=True
    )
# Tab 3 — InfluxDB Dashboard
with tab3:
    st.subheader("InfluxDB Condition Monitoring Dashboard")

    st.info(
        "💡 Click **Open Full Interactive Dashboard** for the complete Tableau experience, including full-screen view, filters, and export options."
    )

    st.link_button(
        "🔗 Open Full Interactive Dashboard",
        "https://public.tableau.com/views/InfluxDB_Condition_Monitoring/InfluxDBConditionMonitoringDashboard?:showVizHome=no"
    )

    components.iframe(
                    "https://public.tableau.com/views/InfluxDB_Condition_Monitoring/InfluxDBConditionMonitoringDashboard?:showVizHome=no",
        height=1100,
        scrolling=True
    )

st.divider()

# --------------------------------------------------
# EXECUTIVE SUMMARY
# --------------------------------------------------

st.header("Executive Summary")

if prediction == "Healthy":

    st.success("""
✅ Overall system status is healthy.

No maintenance action is currently required.
""")

else:

    st.warning(f"""
⚠ Fault Detected : {prediction}

Prediction Confidence : {confidence:.2f}%

Current Spare Stock : {stock}

Work Order : {work_order}

Status : {work_status}

Email Notifications : {email_count} sent
""")
conn.close()

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)