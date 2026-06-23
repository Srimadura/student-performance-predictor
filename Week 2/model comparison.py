import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score

# Load data
df = pd.read_csv("processed_student_data.csv")

# Best feature set
X = df[["Attendance", "StudyHours", "PreviousMarks"]]

y = df["Performance"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Scaling for Logistic Regression
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Logistic Regression
lr = LogisticRegression(max_iter=1000)

lr.fit(X_train_scaled, y_train)

lr_pred = lr.predict(X_test_scaled)

lr_acc = accuracy_score(y_test, lr_pred)

# Decision Tree
dt = DecisionTreeClassifier(random_state=42)

dt.fit(X_train, y_train)

dt_pred = dt.predict(X_test)

dt_acc = accuracy_score(y_test, dt_pred)

print("\nModel Comparison")
print("---------------------------")

print("Logistic Regression Accuracy:", lr_acc)

print("Decision Tree Accuracy:", dt_acc)

if dt_acc > lr_acc:
    print("\nDecision Tree performed better.")

elif lr_acc > dt_acc:
    print("\nLogistic Regression performed better.")

else:
    print("\nBoth models performed equally.")
