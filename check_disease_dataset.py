from pathlib import Path
from PIL import Image
from collections import Counter

ROOT = Path(r"C:\Users\Device\agriSmart\dataset\PlantVillage")

VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

class_counts = Counter()
extension_counts = Counter()
corrupted = []
non_image_files = []

print("Scanning dataset...")
print(f"Dataset: {ROOT}")
print()

for file in ROOT.rglob("*"):
    if not file.is_file():
        continue

    ext = file.suffix.lower()

    if ext not in VALID_EXTENSIONS:
        non_image_files.append(file)
        continue

    extension_counts[ext] += 1

    # Class = first directory directly under PlantVillage
    relative_parts = file.relative_to(ROOT).parts

    if len(relative_parts) < 2:
        continue

    class_name = relative_parts[0]

    try:
        with Image.open(file) as img:
            img.verify()

        class_counts[class_name] += 1

    except Exception:
        corrupted.append(file)


print("=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

print(f"Classes found       : {len(class_counts)}")
print(f"Valid images        : {sum(class_counts.values())}")
print(f"Corrupted images    : {len(corrupted)}")
print(f"Non-image files     : {len(non_image_files)}")

print()
print("=" * 70)
print("CLASS DISTRIBUTION")
print("=" * 70)

for class_name, count in sorted(class_counts.items(), key=lambda x: x[1]):
    print(f"{count:5d}  {class_name}")

print()
print("=" * 70)
print("IMAGE EXTENSIONS")
print("=" * 70)

for ext, count in extension_counts.items():
    print(f"{ext:8s} {count}")

print()

if class_counts:
    minimum = min(class_counts.values())
    maximum = max(class_counts.values())

    print("=" * 70)
    print("BALANCE ANALYSIS")
    print("=" * 70)

    print(f"Minimum class size : {minimum}")
    print(f"Maximum class size : {maximum}")
    print(f"Imbalance ratio    : {maximum / minimum:.2f}:1")

    print()
    print("Threshold analysis:")

    for class_name, count in sorted(class_counts.items(), key=lambda x: x[1]):
        if count < 300:
            status = "VERY LOW"
        elif count < 500:
            status = "LOW"
        elif count < 1000:
            status = "ACCEPTABLE"
        elif count <= 2000:
            status = "GOOD"
        else:
            status = "HIGH"

        print(f"{count:5d}  {status:10s}  {class_name}")

print()

if corrupted:
    print("=" * 70)
    print("CORRUPTED IMAGES")
    print("=" * 70)

    for file in corrupted:
        print(file)

print()
print("Dataset check completed.")