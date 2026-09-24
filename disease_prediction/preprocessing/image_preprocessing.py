import os
from PIL import Image

INPUT_PATH = "datasets/crop_disease/PlantVillage-Dataset/raw/color"
OUTPUT_PATH = "datasets/crop_disease/raw/preprocessed"

IMAGE_SIZE = (224, 224)

os.makedirs(OUTPUT_PATH, exist_ok=True)

total = 0

for class_name in os.listdir(INPUT_PATH):

    class_input = os.path.join(INPUT_PATH, class_name)

    if not os.path.isdir(class_input):
        continue

    class_output = os.path.join(OUTPUT_PATH, class_name)
    os.makedirs(class_output, exist_ok=True)

    for image_name in os.listdir(class_input):

        if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        input_file = os.path.join(class_input, image_name)
        output_file = os.path.join(class_output, image_name)

        try:
            image = Image.open(input_file).convert("RGB")
            image = image.resize(IMAGE_SIZE)
            image.save(output_file)

            total += 1

        except Exception as e:
            print(f"Error: {input_file} -> {e}")

print("=== Image Preprocessing Completed ===")
print(f"Images processed: {total}")
print(f"Image size: {IMAGE_SIZE}")
print(f"Saved to: {OUTPUT_PATH}")