
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

INPUT_FILE = "datasets/crop_recommendation/raw/Crop_recommendation.csv"
OUTPUT_DIR = "datasets/crop_recommendation/processed"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=== Original Dataset ===")
print("Shape:", df.shape)

# --------------------------------------------------
# 3. Select input features and target
# --------------------------------------------------

features = [
    "N",
    "P",
    "K",
    "temperature",
    "humidity",
    "ph",
    "rainfall"
]

X = df[features]
y = df["label"]

# --------------------------------------------------
# 4. Encode crop labels
# --------------------------------------------------

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("\n=== Crop Label Mapping ===")

for number, crop in enumerate(label_encoder.classes_):
    print(f"{number} -> {crop}")

# --------------------------------------------------
# 5. Split dataset
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print("\n=== Data Split ===")
print("Training features:", X_train.shape)
print("Testing features :", X_test.shape)
print("Training labels   :", y_train.shape)
print("Testing labels    :", y_test.shape)

# --------------------------------------------------
# 6. Save processed datasets
# --------------------------------------------------

X_train.to_csv(
    os.path.join(OUTPUT_DIR, "X_train.csv"),
    index=False
)

X_test.to_csv(
    os.path.join(OUTPUT_DIR, "X_test.csv"),
    index=False
)

pd.DataFrame({"label": y_train}).to_csv(
    os.path.join(OUTPUT_DIR, "y_train.csv"),
    index=False
)

pd.DataFrame({"label": y_test}).to_csv(
    os.path.join(OUTPUT_DIR, "y_test.csv"),
    index=False
)

# Save label mapping
label_mapping = pd.DataFrame({
    "encoded_label": range(len(label_encoder.classes_)),
    "crop": label_encoder.classes_
})

label_mapping.to_csv(
    os.path.join(OUTPUT_DIR, "label_mapping.csv"),
    index=False
)

print("\n=== Files Saved ===")
print("X_train.csv")
print("X_test.csv")
print("y_train.csv")
print("y_test.csv")
print("label_mapping.csv")

print("\nPreprocessing completed successfully!")

