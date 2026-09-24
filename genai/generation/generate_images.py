import os
import base64
from openai import OpenAI

OUTPUT_PATH = "datasets/crop_disease/raw/synthetic/Tomato___Tomato_mosaic_virus"

os.makedirs(OUTPUT_PATH, exist_ok=True)

client = OpenAI()

prompt = """
Create a realistic agricultural photograph of a tomato leaf affected by
Tomato Mosaic Virus.

The leaf should show realistic mosaic symptoms with irregular light-green
and dark-green patterns. Show natural leaf texture and realistic lighting.

The image should look like a real crop-disease dataset photograph.
No text, no labels, no watermark, no diagrams, no people.
Focus clearly on the tomato leaf.
"""

print("Generating test image...")

result = client.images.generate(
    model="gpt-image-2",
    prompt=prompt,
    size="1024x1024"
)

image_data = result.data[0].b64_json
image_bytes = base64.b64decode(image_data)

output_file = os.path.join(
    OUTPUT_PATH,
    "synthetic_001.png"
)

with open(output_file, "wb") as f:
    f.write(image_bytes)

print("Image generated successfully!")
print("Saved to:", output_file)