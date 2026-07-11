import pandas as pd
from transformers import pipeline

# Load dataset
df = pd.read_csv("student_feedback.csv")

# Load pre-trained BERT sentiment analysis pipeline
classifier = pipeline("sentiment-analysis")

print("Student Feedback Sentiment Analysis\n")

# Analyze each feedback
for index, row in df.iterrows():

    feedback = row["Feedback"]

    result = classifier(feedback)

    predicted = result[0]["label"]
    confidence = result[0]["score"]

    print(f"Feedback : {feedback}")
    print(f"Actual Sentiment : {row['Sentiment']}")
    print(f"BERT Prediction : {predicted}")
    print(f"Confidence : {confidence:.2f}")
    print("-" * 50)
