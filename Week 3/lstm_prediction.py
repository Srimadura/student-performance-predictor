import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load dataset
df = pd.read_csv("attendance_history.csv")

# Use PerformanceScore for prediction
data = df["PerformanceScore"].values.reshape(-1,1)

# Scale values
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

sequence_length = 5

X = []
y = []

for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i])
    y.append(scaled_data[i])

X = np.array(X)
y = np.array(y)

# Build LSTM model
model = Sequential()

model.add(LSTM(50, activation="relu", input_shape=(sequence_length,1)))

model.add(Dense(1))

model.compile(optimizer="adam", loss="mse")

# Train model
model.fit(X, y, epochs=100, verbose=1)

# Last 5 weeks
last_sequence = scaled_data[-sequence_length:]

last_sequence = last_sequence.reshape(1, sequence_length, 1)

prediction = model.predict(last_sequence)

prediction = scaler.inverse_transform(prediction)

print("Predicted Next Week Performance Score:", round(prediction[0][0],2))

if prediction[0][0] >= 75:
    print("Predicted Performance: Good")
elif prediction[0][0] >= 55:
    print("Predicted Performance: Average")
else:
    print("Predicted Performance: Poor")
