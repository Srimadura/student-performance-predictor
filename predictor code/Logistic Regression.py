import pandas as pd
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("dataset.csv")

X = data[["Attendance","StudyHours","PreviousMarks"]]
y = data["Performance"]

model = LogisticRegression()


model.fit(X,y)

prediction = model.predict([[22,2,5]])

print("Predicted Performance on the given academic data:",prediction[0])
