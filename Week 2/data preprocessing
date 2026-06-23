import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("student_performance.csv")

print("Dataset:")
print(df)

# Check information
print("\nDataset Info:")
print(df.info())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Encode target variable
le = LabelEncoder()
df["Performance"] = le.fit_transform(df["Performance"])

print("\nEncoded Dataset:")
print(df)

# Features and Target
X = df[["Attendance", "StudyHours", "PreviousMarks"]]
y = df["Performance"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Feature Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("\nPreprocessing Completed Successfully!")
print("Training Samples:", len(X_train))
print("Testing Samples:", len(X_test))
