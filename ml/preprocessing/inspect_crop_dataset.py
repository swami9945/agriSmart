import pandas as pd

DATASET_PATH = "datasets/crop_recommendation/raw/Crop_recommendation.csv"


def main():
    df = pd.read_csv(DATASET_PATH)

    print("=== Dataset Shape ===")
    print(df.shape)
    print()

    print("=== Column Names ===")
    print(df.columns.tolist())
    print()

    print("=== First 5 Rows ===")
    print(df.head())
    print()

    print("=== Data Types ===")
    print(df.dtypes)
    print()

    print("=== Missing Values ===")
    print(df.isnull().sum())
    print()

    print("=== Duplicate Rows ===")
    print(f"Number of duplicate rows: {df.duplicated().sum()}")
    print()

    print("=== Unique Crop Classes ===")
    print(f"Number of unique crop classes: {df['label'].nunique()}")
    print()

    print("=== Count of Records for Each Crop ===")
    print(df['label'].value_counts())
    print()

    print("=== Basic Statistical Summary (Numerical Columns) ===")
    print(df.describe(include=["number"]))


if __name__ == "__main__":
    main()
