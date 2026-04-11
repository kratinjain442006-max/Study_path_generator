import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Study Planner", layout="centered")

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- DARK MODE ----------------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    h1,h2,h3,h4,h5,h6,p,label { color:white !important; }

    .stTextInput input, .stNumberInput input {
        background-color:#1e293b !important;
        color:white !important;
    }

    .stButton>button {
        background: linear-gradient(135deg,#ff4b4b,#ff7b7b);
        color:white;
        border-radius:12px;
        height:3em;
        width:100%;
        font-size:18px;
    }

    .stButton>button:hover {
        transform:scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("📚 AI Study Planner")
st.write("Smart Study Plan + Suggestions 😎")

# ---------------- STUDENT DETAILS ----------------
st.subheader("👤 Student Details")

name = st.text_input("Name")
course = st.text_input("Course")
goal = st.text_input("Goal (e.g. exams, placement)")

# ---------------- INPUT ----------------
st.subheader("📥 Study Input")

subjects = st.text_input("Subjects (comma separated)")
marks = st.text_input("Marks (comma separated)")
hours = st.number_input("Study hours per day", min_value=1)
start_time = st.number_input("Start time (24hr format)", min_value=0, max_value=23, value=8)

# ---------------- BUTTON ----------------
if st.button("🚀 Generate Plan"):
    try:
        subjects_list = [s.strip() for s in subjects.split(",")]
        marks_list = list(map(int, marks.split(",")))

        # PRIORITY
        priority = []
        for m in marks_list:
            if m < 50:
                priority.append(3)
            elif m < 75:
                priority.append(2)
            else:
                priority.append(1)

        total_p = sum(priority)

        # PLAN
        plan = []
        for i in range(len(subjects_list)):
            time_alloc = (priority[i] / total_p) * hours
            plan.append({
                "subject": subjects_list[i],
                "time": round(time_alloc, 2),
                "priority": priority[i]
            })

        st.success("✅ Plan Generated!")

        # ---------------- STUDY PLAN ----------------
        st.subheader("📋 Study Plan + Suggestions")

        for item in plan:
            if item["priority"] == 3:
                suggestion = "🔥 Focus more"
            elif item["priority"] == 2:
                suggestion = "⚡ Practice"
            else:
                suggestion = "✅ Revise"

            st.write(f"**{item['subject']}** → {item['time']} hrs | Priority: {item['priority']}")
            st.caption(suggestion)

        # ---------------- GRAPH ----------------
        st.subheader("📊 Study Distribution")

        df = pd.DataFrame(plan)

        fig = px.bar(
            df,
            x="subject",
            y="time",
            color="priority",
            color_discrete_map={
                "1": "green",
                "2": "orange",
                "3": "red"
            },
            text="time"
        )

        st.plotly_chart(fig)

        # ---------------- DAILY TIMETABLE ----------------
        st.subheader("⏰ Daily Timetable")

        current = start_time

        for item in plan:
            start = int(current)
            end = current + item["time"]

            end_hour = int(end)
            end_min = int((end - end_hour) * 60)

            st.write(f"📘 {item['subject']} → {start}:00 to {end_hour}:{end_min:02d}")

            current = end

        # ---------------- WEEKLY PLANNER ----------------
        st.subheader("📅 Weekly Planner")

        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        weekly = []

        for day in days:
            for item in plan:
                weekly.append({
                    "Day": day,
                    "Subject": item["subject"],
                    "Hours": item["time"]
                })

        weekly_df = pd.DataFrame(weekly)
        st.dataframe(weekly_df)

        # ---------------- WEEKLY GRAPH ----------------
        st.subheader("📊 Weekly Graph")

        fig2 = px.bar(
            weekly_df,
            x="Day",
            y="Hours",
            color="Subject",
            barmode="group"
        )

        st.plotly_chart(fig2)

    except:
        st.error("❌ Invalid input") 
