import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# File paths
DATA_DIR = "datasets/crop_recommendation/processed"
MODEL_DIR = "models/crop_recommendation"

os.makedirs(MODEL_DIR, exist_ok=True)


# Load processed data
X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train.csv"))
X_test = pd.read_csv(os.path.join(DATA_DIR, "X_test.csv"))

y_train = pd.read_csv(os.path.join(DATA_DIR, "y_train.csv"))["label"]
y_test = pd.read_csv(os.path.join(DATA_DIR, "y_test.csv"))["label"]


# Models
models = {
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),

    "Decision Tree": DecisionTreeClassifier(
        random_state=42
    ),

    "KNN": KNeighborsClassifier(
        n_neighbors=5
    ),

    "SVM": SVC(
        kernel="rbf",
        random_state=42
    ),

    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        random_state=42
    )
}


results = []
trained_models = {}


print("=== Crop Recommendation Model Training ===\n")


# Train and evaluate
for name, model in models.items():

    print(f"Training {name}...")

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

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })

    trained_models[name] = model

    print(f"Accuracy: {accuracy:.4f}")
    print()


# Create results table
results_df = pd.DataFrame(results)

print("=== Model Comparison ===")
print(results_df.to_string(index=False))


# Select best model based on accuracy
best_index = results_df["Accuracy"].idxmax()
best_model_name = results_df.loc[best_index, "Model"]
best_model = trained_models[best_model_name]


print("\n=== Best Model ===")
print("Model:", best_model_name)
print(
    "Accuracy:",
    f"{results_df.loc[best_index, 'Accuracy']:.4f}"
)


# Save model comparison
results_df.to_csv(
    os.path.join(MODEL_DIR, "model_comparison.csv"),
    index=False
)


# Save best model
joblib.dump(
    best_model,
    os.path.join(MODEL_DIR, "best_crop_model.pkl")
)


# Save model name
with open(
    os.path.join(MODEL_DIR, "best_model_name.txt"),
    "w"
) as file:
    file.write(best_model_name)


print("\n=== Files Saved ===")
print("model_comparison.csv")
print("best_crop_model.pkl")
print("best_model_name.txt")

print("\nModel training completed successfully!")