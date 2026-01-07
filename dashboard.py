import streamlit as st
import requests
import pandas as pd

# Configuration
API_URL = "http://localhost:8000/api/v1"

st.set_page_config(page_title="Job Tracker Dashboard", layout="wide")

st.title("💼 Job Application Tracker")

# 1. Sidebar - Upload MBOX
st.sidebar.header("Import Data")
uploaded_file = st.sidebar.file_uploader("Upload MBOX File", type=["mbox"])
if uploaded_file is not None:
    if st.sidebar.button("Process MBOX"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{API_URL}/upload", files={"file": uploaded_file})
        if response.status_code == 200:
            st.sidebar.success(f"Imported {response.json().get('count')} jobs!")
        else:
            st.sidebar.error("Failed to process MBOX.")

# 2. Analytics Overview (Enhanced)
st.subheader("📊 Analytics Overview")
try:
    analytics_res = requests.get(f"{API_URL}/analytics")
    if analytics_res.status_code == 200:
        data = analytics_res.json()
        
        # Row 1: High-level Totals
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Apps", data["totalApps"])
        col2.metric("Interviews", data["interviews"], delta=f"{data['responseRate']}% rate")
        col3.metric("Pending", data["pending"])
        col4.metric("Rejections", data["rejected"], delta=f"-{data['rejectionRate']}%", delta_color="inverse")
        
        st.markdown("---") # Visual separator
except:
    st.warning("Could not load analytics. Ensure backend is running.")

# 3. Main Table - View Applications (Fixed)
st.subheader("Recent Applications")
apps_res = requests.get(f"{API_URL}/applications")
if apps_res.status_code == 200:
    apps_data = apps_res.json()
    if apps_data:
        df = pd.DataFrame(apps_data)
        
        # Check which columns actually exist to avoid KeyError
        all_possible_cols = ['company', 'position', 'status', 'applied_date']
        existing_cols = [c for c in all_possible_cols if c in df.columns]
        
        st.dataframe(df[existing_cols], use_container_width=True)
    else:
        st.info("No applications found in database.")

# 4. Manual Entry Form
with st.expander("➕ Add Application Manually"):
    with st.form("manual_entry"):
        company = st.text_input("Company")
        position = st.text_input("Position")
        status = st.selectbox("Status", ["applied", "interview", "rejected", "offer"])
        location = st.text_input("Location")
        notes = st.text_area("Notes")
        
        if st.form_submit_button("Save Application"):
            payload = {
                "company": company,
                "position": position,
                "status": status,
                "location": location,
                "notes": notes
            }
            res = requests.post(f"{API_URL}/applications", json=payload)
            if res.status_code == 200:
                st.success("Application saved!")
                st.rerun()