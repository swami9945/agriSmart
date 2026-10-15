import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --------------------------------------------------
# 1. Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "agrismart_crop_dataset_50000.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. Load Dataset
# --------------------------------------------------
df = pd.read_csv(DATA_PATH)

print("\n========== DATASET INFORMATION ==========")
print("Shape:", df.shape)
print("Columns:", list(df.columns))

# --------------------------------------------------
# 3. Missing Values
# --------------------------------------------------
print("\n========== MISSING VALUES ==========")
missing = df.isnull().sum()
print(missing)

print("\nTotal missing values:", missing.sum())

# --------------------------------------------------
# 4. Duplicate Values
# --------------------------------------------------
print("\n========== DUPLICATES ==========")
duplicates = df.duplicated().sum()
print("Duplicate rows:", duplicates)

# --------------------------------------------------
# 5. Class Balance
# --------------------------------------------------
print("\n========== CLASS BALANCE ==========")

class_counts = df["label"].value_counts().sort_index()
class_percent = df["label"].value_counts(normalize=True).sort_index() * 100

class_balance = pd.DataFrame({
    "Count": class_counts,
    "Percentage": class_percent.round(2)
})

print(class_balance)

class_balance.to_csv(
    RESULTS_DIR / "class_balance.csv"
)

# Class balance plot
plt.figure(figsize=(12, 7))
sns.barplot(
    x=class_balance.index,
    y=class_balance["Count"]
)

plt.xticks(rotation=90)
plt.xlabel("Crop")
plt.ylabel("Number of Samples")
plt.title("Crop Class Distribution")
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "class_balance.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 6. Numerical Feature Statistics
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

print("\n========== DESCRIPTIVE STATISTICS ==========")

stats = df[features].describe().T

stats["median"] = df[features].median()

print(stats)

stats.to_csv(
    RESULTS_DIR / "feature_statistics.csv"
)

# --------------------------------------------------
# 7. Feature Ranges / Threshold-like Values
# --------------------------------------------------
print("\n========== FEATURE RANGES ==========")

range_table = pd.DataFrame({
    "Minimum": df[features].min(),
    "Q1": df[features].quantile(0.25),
    "Median": df[features].median(),
    "Q3": df[features].quantile(0.75),
    "Maximum": df[features].max(),
    "Mean": df[features].mean()
})

print(range_table)

range_table.to_csv(
    RESULTS_DIR / "feature_ranges.csv"
)

# --------------------------------------------------
# 8. IQR Outlier Detection
# --------------------------------------------------
print("\n========== OUTLIER ANALYSIS (IQR) ==========")

outlier_results = []

for feature in features:

    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[feature] < lower_bound) |
        (df[feature] > upper_bound)
    ]

    outlier_count = len(outliers)
    outlier_percentage = (outlier_count / len(df)) * 100

    outlier_results.append({
        "Feature": feature,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower_Bound": lower_bound,
        "Upper_Bound": upper_bound,
        "Outlier_Count": outlier_count,
        "Outlier_Percentage": round(outlier_percentage, 2)
    })

outlier_table = pd.DataFrame(outlier_results)

print(outlier_table)

outlier_table.to_csv(
    RESULTS_DIR / "outlier_analysis.csv",
    index=False
)

# --------------------------------------------------
# 9. Boxplots
# --------------------------------------------------
print("\n========== CREATING BOXPLOTS ==========")

for feature in features:

    plt.figure(figsize=(8, 5))

    sns.boxplot(x=df[feature])

    plt.title(f"Boxplot - {feature}")
    plt.xlabel(feature)

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / f"boxplot_{feature}.png",
        dpi=300
    )

    plt.close()

# --------------------------------------------------
# 10. Histograms
# --------------------------------------------------
print("\n========== CREATING HISTOGRAMS ==========")

for feature in features:

    plt.figure(figsize=(8, 5))

    sns.histplot(
        df[feature],
        kde=True
    )

    plt.title(f"Distribution - {feature}")
    plt.xlabel(feature)
    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / f"histogram_{feature}.png",
        dpi=300
    )

    plt.close()

# --------------------------------------------------
# 11. Correlation Matrix
# --------------------------------------------------
print("\n========== CORRELATION MATRIX ==========")

correlation = df[features].corr()

print(correlation.round(3))

correlation.to_csv(
    RESULTS_DIR / "correlation_matrix.csv"
)

plt.figure(figsize=(10, 8))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Feature Correlation Matrix")
plt.tight_layout()

plt.savefig(
    RESULTS_DIR / "correlation_matrix.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# 12. Dataset Summary
# --------------------------------------------------
print("\n========== FINAL SUMMARY ==========")

print("Dataset shape:", df.shape)
print("Missing values:", df.isnull().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Number of crop classes:", df["label"].nunique())

print("\nEDA completed successfully!")

print("\nResults saved in:")
print(RESULTS_DIR)