import os
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Tomato Leveled Data Healthy.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "tomato"
)

os.makedirs(MODEL_DIR, exist_ok=True)

features = [
    "Soil Moisture",
    "Temperature",
    "Humidity",
    "Nitrogen",
    "Phosphorous",
    "Potassium",
    "pH"
]

print("Loading healthy tomato dataset...")

df = pd.read_csv(DATA_PATH)

print("\nDataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df[features].isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

X = df[features]

print("\nTraining Isolation Forest...")

model = Pipeline([
    ("scaler", StandardScaler()),
    ("isolation_forest", IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42
    ))
])

model.fit(X)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "tomato_healthy_anomaly.joblib"
)

joblib.dump(model, MODEL_PATH)

print("\nTraining completed successfully!")

print("\nHealthy samples used:", len(X))

print("\nModel saved at:")
print(MODEL_PATH)