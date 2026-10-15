import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from logic import generate_study_plan, build_daily_timetable
from data import get_sample_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StudyPathAI | Smart Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- SESSION STATE ----------------
DEFAULTS = {
    "logged_in": False,
    "generated_plan": None,
    "student_profile": {},
    "completed_tasks": set(),
    "dark_mode": False,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- STYLES ----------------
def apply_styles(dark: bool):
    if dark:
        background = "#0b1220"
        panel = "#121c2e"
        text = "#edf2ff"
        muted = "#a9b6cc"
        border = "#26354d"
        accent = "#7c9cff"
    else:
        background = "#f5f7fb"
        panel = "#ffffff"
        text = "#172033"
        muted = "#62708a"
        border = "#e3e8f2"
        accent = "#365cf5"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {background};
            color: {text};
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        [data-testid="stSidebar"] {{
            background: {panel};
            border-right: 1px solid {border};
        }}
        h1, h2, h3, h4, p, label, li {{
            color: {text};
        }}
        .hero {{
            padding: 1.35rem 1.5rem;
            border: 1px solid {border};
            border-radius: 20px;
            background: {panel};
            margin-bottom: 1rem;
        }}
        .hero-kicker {{
            color: {accent};
            font-size: .82rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: .08em;
        }}
        .hero-title {{
            font-size: 2rem;
            font-weight: 800;
            margin: .25rem 0;
            color: {text};
        }}
        .hero-copy {{
            color: {muted};
            margin: 0;
        }}
        .metric-card {{
            background: {panel};
            border: 1px solid {border};
            border-radius: 16px;
            padding: 1rem 1.1rem;
            min-height: 112px;
        }}
        .metric-label {{
            color: {muted};
            font-size: .9rem;
