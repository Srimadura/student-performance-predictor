import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv("dataset.csv")

X = data[["Attendance","StudyHours","PreviousMarks"]]
y = data["Performance"]

model = DecisionTreeClassifier()

model.fit(X,y)

prediction = model.predict([[85,4,75]])

print("Predicted Performance:",prediction[0])

