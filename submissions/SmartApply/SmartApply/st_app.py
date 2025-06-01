import streamlit as st
import pandas as pd
import subprocess
import ast
import os

# --- User Data Functions ---
def load_user_data():
    with open("userData.py", "r") as f:
        file_contents = f.read()
        data_dict = ast.literal_eval(file_contents.split("=", 1)[1].strip())
        return data_dict

def save_user_data(updated_data):
    with open("userData.py", "w") as f:
        f.write(f"personal_details = {updated_data}")

# --- User Preferences Modal ---
def show_user_preferences():
    with st.sidebar:
        st.title("User Preferences")
        data = load_user_data()
        
        st.subheader("Edit User Details:")
        updated_data = {}
        for key, value in data.items():
            updated_data[key] = st.text_input(label=key.capitalize(), value=value)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Update"):
                save_user_data(updated_data)
                st.success("User data updated successfully!")
        with col2:
            if st.button("Close"):
                st.session_state.show_preferences = False
                st.rerun()
        
        st.markdown("### Current Saved Data")
        st.json(updated_data)

# Load data
df = pd.read_csv("JobsData.csv")

# Set default view
st.set_page_config(layout="wide", page_title="AI-Powered Job Board", initial_sidebar_state="collapsed")

# Add empty space at the top
st.markdown("<div style='padding-top: 2.5rem;'></div>", unsafe_allow_html=True)

# Title and Preferences button
col1, col2 = st.columns([10, 1])
with col1:
    st.title("💼 Tej.AI-Powered Job Board")
with col2:
    if st.button("⚙️ User Preferences"):
        if 'show_preferences' not in st.session_state:
            st.session_state.show_preferences = True
        else:
            st.session_state.show_preferences = not st.session_state.show_preferences
        st.rerun()

# Show preferences if toggled
if 'show_preferences' in st.session_state and st.session_state.show_preferences:
    show_user_preferences()
    st.stop()

# Custom CSS for styling
st.markdown("""
<style>
    /* Main layout fixes */
    [data-testid="stAppViewContainer"] > .main {
        padding-top: 1rem;
    }
    
    header[data-testid="stHeader"] {
        height: 0;
        visibility: hidden;
    }
    
    .stApp {
        background: linear-gradient(to bottom, #f9fafc, #f0f4ff);
    }
    
    .block-container {
        max-width: 100% !important;
    }
    
    /* Global font improvements */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a;
    }
    
    /* Job card styling */
    .job-card {
        border-left: 4px solid #4361ee;
        padding: 14px 16px;
        margin-bottom: 12px;
        border-radius: 0 8px 8px 0;
        background-color: #f8fafc;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .job-card:hover {
        background-color: #f1f5f9;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .job-card.selected {
        background-color: #e0e7ff;
        border-left: 4px solid #3730a3;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .job-title {
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 4px;
        color: #1e40af;
    }
    .company-name {
        font-size: 15px;
        color: #475569;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .job-location {
        font-size: 14px;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .job-location:before {
        content: '📍';
        font-size: 12px;
    }
    .match-badge {
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #4361ee, #3730a3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Scrollable columns */
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child,
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2) {
        overflow-y: auto !important;
        height: calc(100vh - 180px) !important;
        padding-right: 10px;
        scrollbar-width: thin;
    }
    
    /* Custom scrollbars */
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar,
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar {
        width: 6px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar-track,
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar-thumb,
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar-thumb:hover,
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Job details styling */
    .job-header h2 {
        color: #1e3a8a;
        font-weight: 700;
        font-size: 28px;
        line-height: 1.2;
    }
    .job-meta {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    .job-meta-item {
        font-size: 18px;
        color: #475569;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #4361ee, #3730a3) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 6px 16px !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    .stButton button:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Ensure selected job is tracked
if 'selected_job_id' not in st.session_state:
    st.session_state.selected_job_id = df.iloc[0]['Job_ID']

# --- UI Layout ---
left_col, right_col = st.columns([1.5, 3])

# Left Column: Job List
with left_col:
    st.subheader("🎯 Available Positions", anchor=False)
    left_container = st.container()
    with left_container:
        for idx, row in df.iterrows():
            selected = row['Job_ID'] == st.session_state.selected_job_id
            card_class = "job-card selected" if selected else "job-card"
            col1, col2 = st.columns([10, 3])
            with col1:
                st.markdown(f"""
                <div class="{card_class}" onclick="window.streamlitScriptHost.requestUpdate('set_selected_job', '{row['Job_ID']}')">
                    <div class="job-title">{row['Title']}</div>
                    <div class="company-name">{row['Company']}</div>
                    <div class="job-location">{row['Location']}</div>
                    <span class="match-badge">{row['score']}% Match</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Select", key=f"select_{row['Job_ID']}"):
                    st.session_state.selected_job_id = row['Job_ID']

# Right Column: Job Details
with right_col:
    job = df[df['Job_ID'] == st.session_state.selected_job_id].iloc[0]
    right_container = st.container()
    with right_container:
        st.markdown(f'<div class="job-header"><h2>{job["Title"]}</h2></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"""
            <div class="job-meta">
                <span class="job-meta-item">🏢{job['Company']}</span>
                <span>•</span>
                <span class="job-meta-item">📍{job['Location']}</span>
                <span class="match-badge">✨{job['score']}% Match</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"[🔗 View Job Posting]({job['Apply_URL']})")

        with col2:
            if job['status'].strip().lower() == "applied":
                st.success("Applied")
            else:
                if st.button("Apply Now", use_container_width=True):
                    st.success(f"Applying to {job['Title']}")
                    subprocess.run(["python", "app.py", str(job.name)])
                    st.rerun()
        
        st.markdown("#### 🎯Match Reason")
        st.info(job['reason'])
        
        if pd.notna(job['recruiter_email']) and job['recruiter_email'].strip():
            st.markdown("#### Recruiter Contact")
            st.code(job['recruiter_email'])
        
        view_option = st.radio(
            "",
            ["Job Description", "Cover Letter"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if view_option == "Job Description":
            st.markdown("#### Description")
            st.markdown(job['Description'])
        else:
            st.markdown("#### Cover Letter")
            st.markdown(job['Coverletter'])