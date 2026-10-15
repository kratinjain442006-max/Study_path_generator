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
        }}
        .metric-value {{
            color: {text};
            font-size: 1.7rem;
    font-weight: 800;
            margin-top: .2rem;
        }}
        .metric-help {{
            color: {muted};
            font-size: .8rem;
        }}
        div.stButton > button {{
            border-radius: 10px;
            font-weight: 650;
            min-height: 2.6rem;
        }}
        div[data-testid="stForm"] {{
            border: 1px solid {border};
            border-radius: 14px;
            padding: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_styles(st.session_state.dark_mode)

# ---------------- LOGIN ----------------
def login_page():
    left, center, right = st.columns([1, 1.15, 1])
    with center:
        st.markdown(
            """
            <div class="hero">
              <div class="hero-kicker">Personal learning workspace</div>
              <div class="hero-title">📚 StudyPathAI</div>
              <p class="hero-copy">Build a realistic study routine, focus on weaker subjects, and track your learning.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Login", use_container_width=True)
        if submitted:
            # Demo credentials retained from the original project.
            # Replace with Streamlit secrets or a proper auth provider before public use.
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password.") 
 st.caption("Demo login: username `admin` · password `1234`");
        st.info("Note: this is a demo login, not secure production authentication.")

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 📚 StudyPathAI")
    st.caption("Your personal study companion")
    st.session_state.dark_mode = st.toggle("🌙 Dark mode", value=st.session_state.dark_mode)
    apply_styles(st.session_state.dark_mode)
    st.divider()
    page = st.radio(
        "Navigate",
        ["Dashboard", "Create Study Plan", "My Study Tasks", "About Project"],
        label_visibility="visible",
    )
    st.divider()
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- HELPERS ----------------
def metric_card(label, value, help_text=""):
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-help">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def plan_exists():
    return bool(st.session_state.generated_plan)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
          <div class="hero-kicker">Plan smarter · Learn consistently</div>
          <div class="hero-title">Welcome to your study dashboard 👋</div>
          <p class="hero-copy">Turn your subjects and available hours into a structured, priority-based study plan.</p>
        </div>
        """, 
        unsafe_allow_html=True,
    )

    if plan_exists():
        plan = st.session_state.generated_plan
        tasks = st.session_state.completed_tasks
        total_tasks = len(plan)
        completed = sum(1 for i in range(total_tasks) if i in tasks)
        completion = completed / total_tasks if total_tasks else 0
        total_hours = sum(item["time"] for item in plan)
        high_count = sum(1 for item in plan if item["priority"] == "High")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Subjects planned", total_tasks)
        with c2:
            metric_card("Daily study time", f"{total_hours:.1f} hrs")
        with c3:
            metric_card("High-priority subjects", high_count)
        with c4:
            metric_card("Tasks completed", f"{completion:.0%}", f"{completed} of {total_tasks} subjects marked done")

        st.subheader("Your progress")
        st.progress(completion, text=f"{completion:.0%} of planned subjects completed")
        df = pd.DataFrame(plan)
        fig = px.bar(
            df,
            x="subject",
            y="time",
            color="priority",
            text="time",
            category_orders={"priority": ["High", "Medium", "Low"]},
            color_discrete_map={"High": "#e45756", "Medium": "#f2a541", "Low": "#36a269"},
            labels={"subject": "Subject", "time": "Estimated hours", "priority": "Priority"},
            title="Recommended daily study time by subject",
        )
        fig.update_traces(texttemplate="%{text:.2f} h", textposition="outside", cliponaxis=False)
        fig.update_layout(margin=dict(l=10, r=10, t=55, b=10), height=360)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Tip: mark subjects complete in **My Study Tasks**. Progress is kept during this browser session; permanent saving is not configured yet.")
    else:
        st.info("You haven't generated a study plan yet. Open **Create Study Plan** to get started.")
        st.button("Create my first plan", on_click=lambda: st.session_state.update({"_nav_to_create": True}))
        if st.session_state.pop("_nav_to_create", False):
            st.info("Choose **Create Study Plan** from the sidebar to continue.")

# ---------------- CREATE PLAN ----------------
elif page == "Create Study Plan":
    st.title("✨ Create your personalized study plan")
    st.write("Enter your subjects and current marks. Lower marks receive more study time.")
    sample_subjects, sample_marks, sample_hours = get_sample_data() 

with st.form("plan_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Student name", value=st.session_state.student_profile.get("name", ""))
            course = st.text_input("Course / semester", value=st.session_state.student_profile.get("course", ""))
            goal = st.text_input("Learning goal", value=st.session_state.student_profile.get("goal", "Prepare for exams"))
        with col2:
            subjects_text = st.text_input(
                "Subjects (comma-separated)",
                value=", ".join(sample_subjects),
                help="Example: Computer Networks, Machine Learning, RDBMS",
            )
            marks_text = st.text_input(
                "Marks out of 100 (comma-separated)",
                value=", ".join(map(str, sample_marks)),
                help="Enter one mark for each subject, in the same order.",
            )
            daily_hours = st.number_input("Available study hours per day", min_value=1.0, max_value=16.0, value=float(sample_hours), step=0.5)
            start_hour = st.number_input("Start hour (24-hour clock)", min_value=0, max_value=23, value=8, step=1)

        submitted = st.form_submit_button("🚀 Generate my study plan", use_container_width=True)

    if submitted:
        subjects = [s.strip() for s in subjects_text.split(",") if s.strip()]
        try:
            marks = [float(x.strip()) for x in marks_text.split(",") if x.strip()]
            if not subjects:
                st.error("Please enter at least one subject.")
            elif len(subjects) != len(marks):
                st.error(f"You entered {len(subjects)} subjects but {len(marks)} marks. Please provide one mark per subject.")
            elif any(m < 0 or m > 100 for m in marks):
                st.error("Marks must be between 0 and 100.")
            elif len({s.casefold() for s in subjects}) != len(subjects):
                st.error("Duplicate subject names found. Please use unique subject names.")
            else:
                plan = generate_study_plan(subjects, marks, daily_hours)
                timetable = build_daily_timetable(plan, int(start_hour))
                st.session_state.generated_plan = plan
                st.session_state.student_profile = {"name": name.strip(), "course": course.strip(), "goal": goal.strip()}
                st.session_state.completed_tasks = set()
                st.session_state.daily_timetable = timetable
                st.success("Your study plan is ready!")
                st.rerun()
        except ValueError:
            st.error("Please enter valid numeric marks separated by commas.")

    if plan_exists():
        st.divider()
        st.subheader("Latest generated plan") 
st.caption("Estimated durations are recommendations and can be adjusted to your learning pace.")
        plan = st.session_state.generated_plan
        st.dataframe(
            pd.DataFrame([
                {
                    "Subject": x["subject"],
                    "Current marks": x["marks"],
                    "Priority": x["priority"],
                    "Estimated time (hours)": x["time"],
                    "Suggested action": x["suggestion"],
                }
                for x in plan
            ]),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("⏰ Daily timetable")
        timetable = st.session_state.get("daily_timetable", [])
        if timetable:
            for item in timetable:
                st.write(f"**{item['start']} – {item['end']}** · {item['subject']} · {item['hours']:.2f} hours")
        st.caption("The timetable uses continuous study blocks. Consider adding breaks between subjects.")

# ---------------- TASKS ----------------
elif page == "My Study Tasks":
    st.title("✅ My Study Tasks")
    if not plan_exists():
        st.info("Generate a study plan first, then your subjects will appear here as tasks.")
    else:
        plan = st.session_state.generated_plan
        st.write("Mark a subject complete when you've finished its planned study session.")
        for i, item in enumerate(plan):
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"### {item['subject']}")
                    st.caption(f"{item['priority']} priority · Estimated time: {item['time']:.2f} hours")
                    st.write(item["suggestion"])
                with col2:
                    checked = st.checkbox("Completed", key=f"task_{i}", value=(i in st.session_state.completed_tasks))
                    if checked:
                        st.session_state.completed_tasks.add(i)
                    else:
                        st.session_state.completed_tasks.discard(i)
        done = len(st.session_state.completed_tasks)
        total = len(plan)
        st.progress(done / total if total else 0, text=f"{done}/{total} subjects completed ({(done / total if total else 0):.0%})")
        st.warning("Progress currently lasts for this Streamlit browser session only. A database is needed to retain it reliably after a new session or deployment restart.")

# ---------------- ABOUT ----------------
elif page == "About Project":
    st.title("ℹ️ About StudyPathAI") 
