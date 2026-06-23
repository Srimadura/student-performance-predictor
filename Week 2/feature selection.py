import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load processed data
df = pd.read_csv("processed_student_data.csv")

feature_sets = {
    "All Features":
        ["Attendance", "StudyHours", "PreviousMarks"],

    "Attendance + PreviousMarks":
        ["Attendance", "PreviousMarks"],

    "PreviousMarks Only":
        ["PreviousMarks"]
}

print("Feature Selection Results\n")

for name, features in feature_sets.items():

    X = df[features]
    y = df["Performance"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = DecisionTreeClassifier(random_state=42)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print(f"{name}")
    print(f"Accuracy: {accuracy:.2f}")
    print("-" * 30)
