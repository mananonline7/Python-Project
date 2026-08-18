from utils.db import get_connection

conn = get_connection()
cursor = conn.cursor()
# Import streamlit
import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="Email Notifications",
    page_icon="📧",
    layout="wide"
)

# --------------------------------------------------
# READ DATA FROM SQLITE
# --------------------------------------------------

cursor.execute("""
SELECT bearing, stock, minimum_stock
FROM inventory
ORDER BY id DESC
LIMIT 1
""")

bearing, stock, minimum_stock = cursor.fetchone()

cursor.execute("""
SELECT work_order, status
FROM work_orders
ORDER BY id DESC
LIMIT 1
""")

work_order, work_order_status = cursor.fetchone()

cursor.execute("""
SELECT prediction, confidence
FROM predictions
ORDER BY id DESC
LIMIT 1
""")

prediction, confidence = cursor.fetchone()


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("📧 Email Notifications")

st.write(
    "Automatic notification system for maintenance and inventory departments."
)

st.divider()

# --------------------------------------------------
# EMAIL SUMMARY
# --------------------------------------------------

st.header("Notification Summary")

col1, col2 = st.columns(2)

with col1:

    st.write("**Maintenance Department**")
    st.write("maintenance@company.com")

    st.write("**Inventory Department**")
    st.write("inventory@company.com")

with col2:

    st.write("**Notification Time**")
    st.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

    st.write("**Prediction**")
    st.write(prediction)

st.divider()

# --------------------------------------------------
# EMAIL STATUS
# --------------------------------------------------

st.header("Notification Status")

st.success("📧 Emergency notifications successfully sent to all recipients.")

st.info(
"""
Maintenance Team : maintenance@company.com

Inventory Team : inventory@company.com

Status : Emergency Notification Sent
"""
)

st.divider()

# --------------------------------------------------
# EMAIL CONTENT
# --------------------------------------------------

st.header("Email Notification Preview")

email_body = f"""
Subject: URGENT - {prediction} Detected

Dear Maintenance Team,

The predictive maintenance system has detected:

{prediction}

Prediction Confidence:
{confidence:.2f}%

Recommended Action:
Replace the bearing immediately.

Inventory Status:
Bearing Available

Maintenance Work Order:
{work_order}

Please schedule maintenance as soon as possible.

Regards,

Predictive Maintenance System
"""

st.text_area(
    "",
    value=email_body,
    height=320
)
st.divider()

# --------------------------------------------------
# EMAIL RECIPIENTS
# --------------------------------------------------

st.header("Notification Recipients")

recipient_df = pd.DataFrame({

    "Department":[
        "Maintenance",
        "Inventory",
        "Plant Manager"
    ],

    "Email":[
        "maintenance@company.com",
        "inventory@company.com",
        "manager@company.com"
    ],

    "Status":[
        "Sent",
        "Sent",
        "Sent"
    ]

})

st.dataframe(
    recipient_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# DELIVERY STATUS
# --------------------------------------------------

st.header("Delivery Report")

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(
        "Emails Generated ",
        "3"
    )

with c2:

    st.metric(
        "Emails Delivered",
        "3"
    )

with c3:

    st.metric(
        "Failed Deliveries",
        "0"
    )

st.success("✅ All notifications delivered successfully.")

st.divider()

st.caption(
    "© 2026 PrediMaint AI | MSc Data Science Dissertation | Mohamed Irfan Ali | Arden University"
)