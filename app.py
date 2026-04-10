import streamlit as st
import pandas as pd
from logic import generate_study_plan

st.markdown("""
<style>

/* Background */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1522202176988-66273c2fd55f");
    background-size: cover;
    background-position: center;
}

/* MAIN CONTENT BOX (THIS IS THE FIX 🔥) */
.main .block-container {
    background-color: rgba(0, 0, 0, 0.75);
    padding: 30px;
    border-radius: 15px;
    max-width: 800px;
    margin: auto;
}

/* TEXT */
h1, h2, h3, label {
    color: white !important;
}

/* INPUT BOX */
input {
    background-color: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 8px;
}

/* BUTTON */
div.stButton > button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 10px;
    font-size: 18px;
    padding: 10px;
}

/* TABLE */
.stDataFrame {
    background-color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True) 

st.markdown("<h1>🎯 AI Study Planner</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:white;'>Smart Study Plan Generator for Students</h3>", unsafe_allow_html=True)

st.markdown("### 📥 Enter Your Details")

subjects = st.text_input("Subjects")
marks = st.text_input("Marks")
hours = st.number_input("Study hours", min_value=1)

if st.button("Generate Plan"):

    subjects_list = [s.strip() for s in subjects.split(",")]
    marks_list = list(map(int, marks.split(",")))

    plan = generate_study_plan(subjects_list, marks_list, hours)

    st.success("✅ Study Plan Generated Successfully!")

    st.subheader("📅 Study Plan")

    for item in plan:
        st.write(f"{item['subject']} → {item['time']} hrs | Priority: {item['priority']}")

    df = pd.DataFrame(plan)
    st.dataframe(df)

    st.subheader("📊 Study Time Distribution")
    st.bar_chart(df.set_index("subject")["time"])  




 