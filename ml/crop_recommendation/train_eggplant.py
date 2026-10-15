import os
import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "Eggplant_Healthy_Cleaned.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "eggplant"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "eggplant_healthy_anomaly.joblib"
)


features = [
    "Temperature",
    "Humidity",
    "Soil Moisture",
    "Light",
    "Nitrogen",
    "Phosphorous",
    "Potassium",
    "pH"
]


print("Loading Eggplant healthy dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())


X = df[features]

print("\nHealthy samples used:", len(X))


model = Pipeline([
    ("scaler", StandardScaler()),
    ("isolation_forest", IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42
    ))
])


print("\nTraining Isolation Forest...")

model.fit(X)


os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, MODEL_PATH)


print("\nModel trained successfully!")
print("Model saved at:")
print(MODEL_PATH)