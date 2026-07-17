import pandas as pd
import joblib
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("dataset.csv")

X = data[["Attendance","StudyHours","PreviousMarks"]]
y = data["Performance"]

model = DecisionTreeClassifier()

model.fit(X,y)

joblib.dump(model,"decision_tree_model.pkl")

print("Model Saved Successfully!")