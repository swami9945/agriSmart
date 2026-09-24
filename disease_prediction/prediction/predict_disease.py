import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

MODEL_PATH = "models/disease_prediction/disease_prediction_model.keras"
CLASS_PATH = "models/disease_prediction/class_names.txt"

IMG_SIZE = (224, 224)

# Load model
model = tf.keras.models.load_model(MODEL_PATH)

# Load class names
with open(CLASS_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]

# Ask for image
image_path = input("Enter leaf image path: ").strip()

if not os.path.exists(image_path):
    print("Image not found!")
    exit()

# Load and preprocess image
img = image.load_img(
    image_path,
    target_size=IMG_SIZE
)

img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Prediction
prediction = model.predict(img_array, verbose=0)

predicted_index = np.argmax(prediction[0])
confidence = prediction[0][predicted_index] * 100

predicted_disease = class_names[predicted_index]

print("\n=== Disease Prediction ===")
print("Predicted Disease:", predicted_disease)
print(f"Confidence: {confidence:.2f}%")