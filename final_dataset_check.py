from pathlib import Path
from PIL import Image
from collections import Counter

ROOT = Path(r"C:\Users\Device\agriSmart\dataset\PlantVillage")
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

counts = Counter()
corrupted = []
non_image = []

for class_dir in ROOT.iterdir():

    if not class_dir.is_dir():
        continue

    # Ignore the duplicate nested PlantVillage folder
    if class_dir.name == "PlantVillage":
        continue

    for file in class_dir.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix.lower() not in VALID_EXTENSIONS:
            non_image.append(file)
            continue

        try:
            with Image.open(file) as img:
                img.verify()

            counts[class_dir.name] += 1

        except Exception:
            corrupted.append(file)

print("=" * 70)
print("FINAL DISEASE DATASET VALIDATION")
print("=" * 70)

print(f"Dataset root       : {ROOT}")
print(f"Classes            : {len(counts)}")
print(f"Valid images       : {sum(counts.values())}")
print(f"Corrupted images   : {len(corrupted)}")
print(f"Non-image files    : {len(non_image)}")

print()
print("-" * 70)
print("CLASS DISTRIBUTION")
print("-" * 70)

for name, count in sorted(counts.items(), key=lambda x: x[1]):
    print(f"{count:5d}  {name}")

minimum = min(counts.values())
maximum = max(counts.values())

print()
print("-" * 70)
print("BALANCE")
print("-" * 70)

print(f"Minimum class      : {minimum}")
print(f"Maximum class      : {maximum}")
print(f"Imbalance ratio    : {maximum / minimum:.2f}:1")

print()
print("-" * 70)
print("THRESHOLD")
print("-" * 70)

for name, count in sorted(counts.items(), key=lambda x: x[1]):

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

    print(f"{count:5d}  {status:12s}  {name}")

print()
print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)

if corrupted:
    print("\nCorrupted files:")
    for file in corrupted:
        print(file)