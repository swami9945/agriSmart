import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


# =========================
# Paths
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR, "data", "agrismart_crop_dataset_combined_52200.csv"
)


MODEL_DIR = os.path.join(BASE_DIR, "models")
RESULT_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)


# =========================
# Load Dataset
# =========================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())


# =========================
# Basic Data Checking
# =========================

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nNumber of crop classes:", df["label"].nunique())

print("\nCrop classes:")
print(sorted(df["label"].unique()))


# Remove duplicates if present
df = df.drop_duplicates().reset_index(drop=True)


# =========================
# Features and Target
# =========================

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


# =========================
# Train/Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# =========================
# Encode labels for XGBoost
# =========================

classes = sorted(y.unique())

label_to_id = {
    label: index
    for index, label in enumerate(classes)
}

id_to_label = {
    index: label
    for label, index in label_to_id.items()
}

y_train_xgb = y_train.map(label_to_id)
y_test_xgb = y_test.map(label_to_id)


# =========================
# Define Models
# =========================

models = {

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    ),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", KNeighborsClassifier(
            n_neighbors=5
        ))
    ]),

    "SVM": Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", SVC(
            kernel="rbf",
            probability=True,
            random_state=42
        ))
    ])
}


# =========================
# Train Scikit-learn Models
# =========================

results = []

for name, model in models.items():

    print("\n" + "=" * 60)
    print("Training:", name)
    print("=" * 60)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )
    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0
    ))

    # Save model
    filename = name.lower().replace(" ", "_") + ".joblib"

    model_path = os.path.join(
        MODEL_DIR,
        filename
    )

    joblib.dump(model, model_path)

    print("Saved:", model_path)

    # Save confusion matrix
    cm = confusion_matrix(
        y_test,
        predictions,
        labels=classes
    )

    cm_path = os.path.join(
        RESULT_DIR,
        name.lower().replace(" ", "_") + "_confusion_matrix.csv"
    )

    pd.DataFrame(
        cm,
        index=classes,
        columns=classes
    ).to_csv(cm_path)

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })


# =========================
# XGBoost
# =========================

print("\n" + "=" * 60)
print("Training: XGBoost")
print("=" * 60)

xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.9,
    colsample_bytree=0.9,
    objective="multi:softprob",
    num_class=len(classes),
    eval_metric="mlogloss",
    random_state=42,
    n_jobs=-1
)

xgb_model.fit(
    X_train,
    y_train_xgb
)

xgb_predictions = xgb_model.predict(X_test)

accuracy = accuracy_score(
    y_test_xgb,
    xgb_predictions
)

precision = precision_score(
    y_test_xgb,
    xgb_predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test_xgb,
    xgb_predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test_xgb,
    xgb_predictions,
    average="weighted",
    zero_division=0
)

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))

print("\nClassification Report:")
print(classification_report(
    y_test_xgb,
    xgb_predictions,
    target_names=classes,
    zero_division=0
))

# Save XGBoost model and label mapping
xgb_path = os.path.join(
    MODEL_DIR,
    "xgboost.joblib"
)

joblib.dump(
    {
        "model": xgb_model,
        "label_to_id": label_to_id,
        "id_to_label": id_to_label,
        "features": features
    },
    xgb_path
)

print("Saved:", xgb_path)

cm = confusion_matrix(
    y_test_xgb,
    xgb_predictions,
    labels=list(range(len(classes)))
)

cm_path = os.path.join(
    RESULT_DIR,
    "xgboost_confusion_matrix.csv"
)

pd.DataFrame(
    cm,
    index=classes,
    columns=classes
).to_csv(cm_path)

results.append({
    "Model": "XGBoost",
    "Accuracy": accuracy,
    "Precision": precision,
    "Recall": recall,
    "F1 Score": f1
})


# =========================
# Model Comparison
# =========================

results_df = pd.DataFrame(results)

print("\n")
print("=" * 70)
print("MODEL COMPARISON")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)

comparison_path = os.path.join(
    RESULT_DIR,
    "model_comparison.csv"
)

results_df.to_csv(
    comparison_path,
    index=False
)

print("\nComparison saved to:")
print(comparison_path)

print("\nTraining completed successfully!")