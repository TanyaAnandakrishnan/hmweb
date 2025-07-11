import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Sample dataset
data = {
    "heart_rate": [55, 75, 95, 115, 135, 160],
    "systolic_bp": [90, 110, 120, 140, 160, 180],
    "diastolic_bp": [60, 75, 80, 90, 100, 120],
    "pulse_rate": [50, 70, 85, 100, 115, 130],
    "emotion": ["Relaxed", "Calm", "Focused", "Happy", "Anxious", "Panic"]
}

df = pd.DataFrame(data)

# Convert emotions to numeric labels
emotion_map = {"Relaxed": 0, "Calm": 1, "Focused": 2, "Happy": 3, "Anxious": 4, "Panic": 5}
df["emotion"] = df["emotion"].map(emotion_map)

# Split dataset
X = df.drop("emotion", axis=1)
y = df["emotion"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "emotion_model.pkl")
print("✅ Model trained and saved as 'emotion_model.pkl'")