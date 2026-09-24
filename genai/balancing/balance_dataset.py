import os
import shutil

REAL_DIR = "datasets/crop_disease/PlantVillage-Dataset/raw/color"
SYNTHETIC_DIR = "datasets/crop_disease/raw/synthetic"
BALANCED_DIR = "datasets/crop_disease/raw/balanced"

os.makedirs(BALANCED_DIR, exist_ok=True)

classes = sorted([
    d for d in os.listdir(REAL_DIR)
    if os.path.isdir(os.path.join(REAL_DIR, d))
])

print("=== Dataset Class Counts ===\n")

for class_name in classes:
    real_path = os.path.join(REAL_DIR, class_name)
    synthetic_path = os.path.join(SYNTHETIC_DIR, class_name)

    real_images = [
        f for f in os.listdir(real_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    synthetic_images = []

    if os.path.exists(synthetic_path):
        synthetic_images = [
            f for f in os.listdir(synthetic_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]

    total = len(real_images) + len(synthetic_images)

    print(
        f"{class_name}: "
        f"Real={len(real_images)}, "
        f"Synthetic={len(synthetic_images)}, "
        f"Total={total}"
    )

print("\n=== Balance Analysis Completed ===")