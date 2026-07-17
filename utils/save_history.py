import pandas as pd
import os

FILE_PATH = "data/student_history.csv"

def save_student_data(student_id, attendance, study_hours, previous_marks, feedback):

    # Create CSV if it doesn't exist
    if not os.path.exists(FILE_PATH):
        df = pd.DataFrame(columns=[
            "StudentID",
            "Week",
            "Attendance",
            "StudyHours",
            "PreviousMarks",
            "Feedback"
        ])
        df.to_csv(FILE_PATH, index=False)

    # Read CSV
    df = pd.read_csv(FILE_PATH)

    # Convert StudentID column to string
    df["StudentID"] = df["StudentID"].astype(str)

    # Find this student's previous records
    student_data = df[df["StudentID"] == str(student_id)]

    # Decide next week
    if len(student_data) == 0:
        week = 1
    else:
        week = int(student_data["Week"].max()) + 1

    # Create new row
    new_row = {
        "StudentID": str(student_id),
        "Week": week,
        "Attendance": attendance,
        "StudyHours": study_hours,
        "PreviousMarks": previous_marks,
        "Feedback": feedback
    }

    # Append row
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save CSV
    df.to_csv(FILE_PATH, index=False)

    return week