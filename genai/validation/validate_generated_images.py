from PIL import Image
import os
import hashlib
import csv

INPUT_DIR = "datasets/crop_disease/raw/synthetic/Tomato___Tomato_mosaic_virus"
OUTPUT_DIR = "datasets/crop_disease/validated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

results = []
hashes = set()

files = [
    f for f in os.listdir(INPUT_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

print("=== Synthetic Image Validation ===")
print("Images found:", len(files))

for filename in sorted(files):
    path = os.path.join(INPUT_DIR, filename)

    try:
        with Image.open(path) as img:
            img.verify()

        with Image.open(path) as img:
            width, height = img.size
            mode = img.mode

        with open(path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        duplicate = file_hash in hashes
        hashes.add(file_hash)

        status = "DUPLICATE" if duplicate else "VALID"

        results.append([
            filename,
            width,
            height,
            mode,
            status
        ])

        print(f"{filename} -> {width}x{height} -> {mode} -> {status}")

    except Exception as e:
        results.append([
            filename,
            "",
            "",
            "",
            f"INVALID: {e}"
        ])

        print(f"{filename} -> INVALID")

report_path = os.path.join(
    OUTPUT_DIR,
    "synthetic_validation_report.csv"
)

with open(report_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "filename",
        "width",
        "height",
        "mode",
        "status"
    ])

    writer.writerows(results)

valid_count = sum(
    1 for row in results if row[4] == "VALID"
)

print("\n=== Validation Completed ===")
print("Total images :", len(files))
print("Valid images :", valid_count)
print("Report saved :", report_path)