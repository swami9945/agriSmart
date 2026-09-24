import os
import pandas as pd

DATASET_PATH = "datasets/crop_disease/PlantVillage-Dataset/raw/color"
OUTPUT_PATH = "datasets/crop_disease/raw/dataset_summary.csv"

records = []

for class_name in sorted(os.listdir(DATASET_PATH)):
    class_path = os.path.join(DATASET_PATH, class_name)

    if not os.path.isdir(class_path):
        continue

    for image_name in os.listdir(class_path):
        if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            records.append({
                "class": class_name,
                "image": image_name,
                "path": os.path.join(class_path, image_name)
            })

df = pd.DataFrame(records)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("=== Disease Dataset Summary ===")
print(f"Total images: {len(df)}")
print(f"Total classes: {df['class'].nunique()}")

print("\n=== Images Per Class ===")
print(df["class"].value_counts().sort_index())

print(f"\nSummary saved to:")
print(OUTPUT_PATH)