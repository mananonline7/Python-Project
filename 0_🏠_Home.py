import streamlit as st

st.set_page_config(
    page_title="PrediMaint AI",
    page_icon="🏭",
    layout="wide"
)

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.title("🏠 PrediMaint AI")
st.subheader("Machine Learning Based Predictive Maintenance Portal")

#st.subheader("Machine Learning Based Predictive Maintenance System")

st.markdown("---")

st.header("📊 Executive Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Prediction",
        "Outer Fault",
        "100%"
    )

with col2:
    st.metric(
        "Open Work Orders",
        "1",
        "High Priority"
    )

with col3:
    st.metric(
        "Inventory Status",
        "8 Bearings",
        "Available"
    )

with col4:
    st.metric(
        "Email Notifications",
        "3 Sent",
        "Delivered"
    )

st.divider()


# -----------------------------------------------------
# SYSTEM STATUS
# -----------------------------------------------------

st.header("🖥️ System Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("🟢 InfluxDB Connected")

with c2:
    st.success("🟢 SQLite Ready")

with c3:
   
    st.success("🟢 Random Forest Loaded")
   
with c4:
    st.success("🟢 Streamlit Running")

st.divider()

# -----------------------------------------------------
# TECHNOLOGY STACK
# -----------------------------------------------------

st.header("⚙ Technology Stack")

left, right = st.columns(2)

with left:

    st.write("✔ Python")

    st.write("✔ Streamlit")

    st.write("✔ InfluxDB 3")

    st.write("✔ SQLite")

with right:

    st.write("✔ Machine Learning")

    st.write("✔ Random Forest")

    st.write("✔ Tableau")

    st.write("✔ Predictive Maintenance")

st.divider()

# -----------------------------------------------------
# NAVIGATION
# -----------------------------------------------------

st.header("🔄 System Workflow")

st.info("""
📈 Live Monitoring

⬇

🤖 Machine Learning Prediction

⬇

🔧 Maintenance Work Orders

⬇

📦 Inventory Management

⬇

📧 Email Notifications

⬇

📊 Tableau Analytics
""")

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)

from datetime import datetime

st.write(
    "🕒 Last Updated:",
    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)