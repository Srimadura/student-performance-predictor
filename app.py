import streamlit as st
import json
import os
import pandas as pd

# File to store student data locally (Memory)
DATA_FILE = "student_records.json"

def load_data():
    """Loads student data from the local JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data):
    """Saves student data to the local JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Load existing database
student_db = load_data()

# App Configuration
st.set_page_config(page_title="Student AI Advisor", page_icon="🎓")
st.title("🎓 Student AI Advisor")
st.write("Track your weekly academic progress and get instant AI-driven recommendations.")

st.markdown("---")

## 1. Student Identification & Week Selection
col1, col2 = st.columns(2)
with col1:
    student_id = st.text_input("Enter Student ID:", value="STU1001").strip().upper()
with col2:
    # Generates Week 1 to Week 16 options
    week_options = [f"Week {i}" for i in range(1, 17)]
    selected_week = st.selectbox("Select Week:", week_options)

# Check if there is already data saved for this student and week (for auto-populating/editing)
existing_data = student_db.get(student_id, {}).get(selected_week, {})

if existing_data:
    st.info(f"ℹ️ Found existing data for {selected_week}. You can modify it below to overwrite errors.")

## 2. Weekly Metrics Input Form
st.subheader(f"📝 Enter Data for {selected_week}")

# Attendance & Study Hours
col3, col4 = st.columns(2)
with col3:
    attendance = st.slider(
        "Attendance Rate (%)", 
        min_value=0, 
        max_value=100, 
        value=int(existing_data.get("attendance", 85))
    )
with col4:
    study_hours = st.number_input(
        "Self-Study Hours (This Week)", 
        min_value=0, 
        max_value=168, 
        value=int(existing_data.get("study_hours", 10))
    )

# Performance Marks
st.markdown("**Previous Marks / Performance This Week:**")
col5, col6, col7 = st.columns(3)
with col5:
    quiz_marks = st.number_input("Quiz Score (out of 20)", min_value=0, max_value=20, value=int(existing_data.get("quiz", 15)))
with col6:
    assignment_marks = st.number_input("Assignment Score (out of 10)", min_value=0, max_value=10, value=int(existing_data.get("assignment", 8)))
with col7:
    exam_marks = st.number_input("Internal Exam (out of 50)", min_value=0, max_value=50, value=int(existing_data.get("exam", 35)))

# Qualitative Feedback
feedback = st.text_area(
    "Your Personal Feedback / Notes (e.g., 'OS was difficult, Maths went well')", 
    value=existing_data.get("feedback", "")
)

st.markdown("---")

## 3. Save & Analyze Engine
if st.button("🔥 Save & Analyze Performance", type="primary"):
    if not student_id:
        st.error("Please enter a valid Student ID before analyzing.")
    else:
        # Initialize student profile if it doesn't exist
        if student_id not in student_db:
            student_db[student_id] = {}
        
        # Save/Overwrite data for the selected week
        student_db[student_id][selected_week] = {
            "attendance": attendance,
            "study_hours": study_hours,
            "quiz": quiz_marks,
            "assignment": assignment_marks,
            "exam": exam_marks,
            "feedback": feedback
        }
        save_data(student_db)
        st.success(f"💾 Data successfully saved/updated for {student_id} ({selected_week})!")

        ## 4. AI Advisor Logic (Rule-Based Insights)
        st.subheader("🤖 AI Advisor Insights")
        insights = []

        # Attendance check
        if attendance < 75:
            insights.append(f"⚠️ **Low Attendance ({attendance}%):** You are below the 75% threshold. Missing more classes might risk your eligibility or final grades. Prioritize attending next week!")
        else:
            insights.append(f"✅ **Good Attendance ({attendance}%):** You are maintaining a solid presence in class. Keep it up.")

        # Study hours check
        if study_hours < 8:
            insights.append(f"⚠️ **Study Deficit ({study_hours} hrs):** Your independent study hours are low this week. Try to carve out at least 2 hours a day to review materials.")
        elif study_hours >= 15:
            insights.append(f"🌟 **Excellent Focus ({study_hours} hrs):** Exceptional dedication! You are putting in great effort outside the classroom.")

        # Grade calculation (Percentage out of total 80 marks)
        total_obtained = quiz_marks + assignment_marks + exam_marks
        score_percentage = (total_obtained / 80) * 100

        if score_percentage < 55:
            insights.append(f"❌ **Academic Performance Alert ({score_percentage:.1f}%):** Your current scores are trending low. It might be time to sync up with a professor or look into tutoring.")
        elif score_percentage >= 85:
            insights.append(f"🎉 **Top Tier Scores ({score_percentage:.1f}%):** Brilliant academic performance across your weekly evaluations!")

        # Sentiment / Keyword parsing from text feedback
        difficult_keywords = ["difficult", "hard", "struggling", "confusing", "failed", "stuck", "os", "maths"]
        flagged_words = [word for word in difficult_keywords if word in feedback.lower()]
        
        if flagged_words:
            insights.append(f"💡 **Subject Action Item:** You noted difficulties regarding core terms/subjects in your log. Don't let these bottlenecks accumulate. Allocate an extra 45 minutes specifically to these problem areas next week.")

        # Display advice cards
        for insight in insights:
            st.info(insight)

st.markdown("---")

## 5. View Student Dashboard History
if student_id in student_db and student_db[student_id]:
    st.subheader(f"📊 Historical Log for Student: {student_id}")
    # Convert student history dictionary to a DataFrame for clean rendering
    df_history = pd.DataFrame.from_dict(student_db[student_id], orient='index')
    # Reordering columns for cleaner visibility
    columns_order = ['attendance', 'study_hours', 'quiz', 'assignment', 'exam', 'feedback']
    st.dataframe(df_history[[col for col in columns_order if col in df_history.columns]])
else:
    st.info("💡 No prior history found for this Student ID yet. Enter data above and click 'Save & Analyze' to start your log.")