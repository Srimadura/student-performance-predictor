import streamlit as st
import pandas as pd
import os

# ---------- Basic setup ----------
st.set_page_config(page_title="Student AI Advisor", page_icon="📚")

DATA_FILE = "student_data.csv"
COLUMNS = [
    "student_id", "week", "attendance", "study_hours",
    "quiz_marks", "assignment_marks", "internal_marks", "feedback"
]

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=COLUMNS)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ---------- Title ----------
st.title("📚 Student AI Advisor")
st.caption("Log your weekly attendance, study hours, marks and feedback. It auto-saves and remembers everything.")

df = load_data()

# ---------- Entry Form ----------
st.header("Weekly Entry")

with st.form("entry_form", clear_on_submit=False):
    col1, col2 = st.columns(2)
    with col1:
        student_id = st.text_input("Student ID")
        week = st.number_input("Week", min_value=1, step=1)
        attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, step=1.0)
        study_hours = st.number_input("Study Hours (this week)", min_value=0.0, step=0.5)
    with col2:
        quiz_marks = st.number_input("Quiz Marks (out of 10)", min_value=0.0, max_value=10.0, step=0.5)
        assignment_marks = st.number_input("Assignment Marks (out of 10)", min_value=0.0, max_value=10.0, step=0.5)
        internal_marks = st.number_input("Internal Exam Marks (out of 50)", min_value=0.0, max_value=50.0, step=1.0)

    feedback = st.text_area("Feedback (e.g. 'OS was difficult, Maths was difficult')")

    submitted = st.form_submit_button("Submit (auto-saves)")

    if submitted:
        if not student_id.strip():
            st.error("Please enter your Student ID.")
        else:
            # Remove any existing row for same student_id + week (so corrections overwrite)
            df = df[~((df["student_id"] == student_id) & (df["week"] == week))]
            new_row = {
                "student_id": student_id, "week": week, "attendance": attendance,
                "study_hours": study_hours, "quiz_marks": quiz_marks,
                "assignment_marks": assignment_marks, "internal_marks": internal_marks,
                "feedback": feedback
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df = df.sort_values(by=["student_id", "week"]).reset_index(drop=True)
            save_data(df)
            st.success(f"Saved Week {week} for {student_id}. (If it existed already, it was updated.)")

# ---------- History ----------
st.header("Your History")
lookup_id = st.text_input("Enter Student ID to view / analyze history", key="lookup")

if lookup_id.strip():
    student_df = df[df["student_id"] == lookup_id].sort_values("week")
    if student_df.empty:
        st.info("No entries found for this Student ID yet.")
    else:
        st.dataframe(student_df.drop(columns=["student_id"]), use_container_width=True)

        # ---------- Analyze ----------
        if st.button("🔍 Analyze"):
            st.subheader("Advisor Feedback")

            avg_attendance = student_df["attendance"].mean()
            avg_study_hours = student_df["study_hours"].mean()
            avg_quiz = student_df["quiz_marks"].mean()
            avg_assignment = student_df["assignment_marks"].mean()
            avg_internal = student_df["internal_marks"].mean()

            notes = []

            # Attendance check
            if avg_attendance < 75:
                notes.append(f"⚠️ Your average attendance is {avg_attendance:.1f}%, which is low. Try to attend more classes regularly.")
            else:
                notes.append(f"✅ Your average attendance is {avg_attendance:.1f}%, which is good.")

            # Study hours check
            if avg_study_hours < 2:
                notes.append(f"⚠️ Your average study hours per week is only {avg_study_hours:.1f}. Consider increasing your study time.")
            elif avg_study_hours < 5:
                notes.append(f"🟡 Your average study hours per week is {avg_study_hours:.1f}. Decent, but could be higher.")
            else:
                notes.append(f"✅ Your average study hours per week is {avg_study_hours:.1f}. Great consistency!")

            # Marks check
            marks_msgs = []
            if avg_quiz < 5:
                marks_msgs.append("quiz marks are low")
            if avg_assignment < 5:
                marks_msgs.append("assignment marks are low")
            if avg_internal < 25:
                marks_msgs.append("internal exam marks are low")

            if marks_msgs:
                notes.append("⚠️ Your " + ", ".join(marks_msgs) + ". Focus more on these areas.")
            else:
                notes.append("✅ You're doing well marks-wise across quizzes, assignments and internals.")

            # Trend check (marks improving or dropping)
            if len(student_df) >= 2:
                internal_trend = student_df["internal_marks"].iloc[-1] - student_df["internal_marks"].iloc[0]
                if internal_trend < 0:
                    notes.append("📉 Your internal exam marks seem to be dropping over the weeks. Keep an eye on this.")
                elif internal_trend > 0:
                    notes.append("📈 Your internal exam marks are improving over the weeks. Keep it up!")

            # Feedback keyword scan (find subjects marked as difficult)
            all_feedback = " ".join(student_df["feedback"].dropna().astype(str)).lower()
            if "difficult" in all_feedback or "hard" in all_feedback or "tough" in all_feedback:
                # crude extraction: find words right before "difficult/hard/tough" or comma-separated mentions
                subjects_found = []
                for chunk in all_feedback.replace(".", ",").split(","):
                    if "difficult" in chunk or "hard" in chunk or "tough" in chunk:
                        subjects_found.append(chunk.strip())
                notes.append("📝 From your feedback, these seem to be trouble spots: " + "; ".join(subjects_found) + ". Consider putting extra effort or seeking help in these subjects.")

            # Combine attendance + marks + hours for an overall verdict
            if avg_attendance < 75 and avg_study_hours < 2:
                notes.append("🚨 Overall: Both your attendance and study hours are low — this is likely affecting your marks. Prioritize fixing these first.")
            elif avg_attendance >= 75 and (avg_quiz >= 5 and avg_assignment >= 5 and avg_internal >= 25):
                notes.append("🎉 Overall: You're on track — good attendance and good marks. Just keep maintaining this pace.")

            for n in notes:
                st.write(n)
else:
    st.caption("Enter your Student ID above to see your saved weeks and get analysis.")