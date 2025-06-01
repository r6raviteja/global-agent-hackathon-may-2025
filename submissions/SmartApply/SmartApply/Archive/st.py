import streamlit as st
import pandas as pd
import subprocess

# Load data
df = pd.read_csv("JobsData.csv")

# Set default view
st.set_page_config(layout="wide", page_title="AI-Powered Job Board", initial_sidebar_state="collapsed")
st.title("💼 Tej.AI-Powered Job Board")

# Add a subtle background color
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #f9fafc, #f0f4ff);
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main layout fixes */
    .block-container {
        padding-top: 1rem;
        max-width: 100% !important;
    }
    .st-emotion-cache-1v0mbdj {
        margin-bottom: 0;
    }
    
    /* Global font improvements */
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #2c3e50;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #1e3a8a;
    }
    
    /* Left column styling with independent scrolling */
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child {
        overflow-y: auto !important;
        height: calc(100vh - 180px) !important;
        padding-right: 10px;
        scrollbar-width: thin;
    }
    
    /* Custom scrollbar for left column */
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar {
        width: 6px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:first-child::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
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
    .match-score {
        font-size: 14px;
        color: #059669;
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Right column styling with independent scrolling */
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2) {
        overflow-y: auto !important;
        height: calc(100vh - 180px) !important;
        padding-left: 20px;
        padding-right: 10px;
        scrollbar-width: thin;
    }
    
    /* Custom scrollbar for right column */
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar {
        width: 6px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 10px;
    }
    .main > div:first-child > div:first-child > div:nth-child(2) > div:nth-child(2)::-webkit-scrollbar-thumb:hover {
        background: #a1a1a1;
    }
    
    /* Job details styling */
    .job-header {
        margin-bottom: 16px !important;
    }
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
    .match-badge {
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #4361ee, #3730a3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .action-row {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        margin-top: 10px;
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
    
    /* Link styling */
    a {
        color: #4361ee !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    a:hover {
        color: #3730a3 !important;
        text-decoration: underline !important;
    }
    
    /* Section styling */
    .stMarkdown h4 {
        color: #1e3a8a;
        font-size: 20px;
        margin-top: 20px;
        margin-bottom: 10px;
        font-weight: 600;
        border-bottom: 2px solid #e0e7ff;
        padding-bottom: 6px;
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* Hide checkbox labels and fix radio */
    .stRadio > div > div > label {
        display: none !important;
    }
    .stRadio > div {
        gap: 10px !important;
    }
    .stRadio > div > div[role="radiogroup"] {
        gap: 10px !important;
    }
    
    /* Radio button styling */
    .stRadio [role="radiogroup"] [data-baseweb="radio"] {
        margin-right: 10px !important;
    }
    .stRadio [role="radiogroup"] [data-baseweb="radio"] [data-baseweb="radio"] {
        background-color: #f8fafc !important;
        border-color: #cbd5e1 !important;
    }
    .stRadio [role="radiogroup"] [data-baseweb="radio"][aria-checked="true"] [data-baseweb="radio"] {
        background-color: #4361ee !important;
        border-color: #4361ee !important;
    }
</style>
""", unsafe_allow_html=True)

# Ensure selected job is tracked
if 'selected_job_id' not in st.session_state:
    st.session_state.selected_job_id = df.iloc[0]['Job_ID']

# --- UI Layout ---
left_col, right_col = st.columns([1.5, 3])

# --------------- LEFT COLUMN: Job List ---------------
with left_col:
    st.subheader("🎯 Available Positions", anchor=False)
    
    # Create job list container
    left_container = st.container()
    with left_container:
        for idx, row in df.iterrows():
            selected = row['Job_ID'] == st.session_state.selected_job_id
            card_class = "job-card selected" if selected else "job-card"
            # Create clickable job card
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
                # Hidden button for selection
                if st.button("Select", key=f"select_{row['Job_ID']}"):
                    st.session_state.selected_job_id = row['Job_ID']

# --------------- RIGHT COLUMN: Job Details ---------------
with right_col:
    job = df[df['Job_ID'] == st.session_state.selected_job_id].iloc[0]
    
    # Create job details container
    right_container = st.container()
    with right_container:
        # Header section - compact
        st.markdown(f'<div class="job-header"><h2>{job["Title"]}</h2></div>', unsafe_allow_html=True)
        
        
        # Action buttons
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
                    #df.loc[job.name, 'status'] = 'applied'
                    # Force a rerun to update the UI
                    st.rerun()
        
            
        
        
        # Match reason
        st.markdown("#### 🎯Match Reason")
        st.info(job['reason'])
        
        # Recruiter info
        if pd.notna(job['recruiter_email']) and job['recruiter_email'].strip():
            st.markdown("#### Recruiter Contact")
            st.code(job['recruiter_email'])
        
        # Toggle between description and cover letter
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