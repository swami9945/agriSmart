import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

DATASET_DIR = "datasets/crop_disease/raw/balanced"
MODEL_DIR = "models/disease_prediction"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

os.makedirs(MODEL_DIR, exist_ok=True)

print("TensorFlow version:", tf.__version__)

# Data augmentation
datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2
)

train_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

validation_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

# CNN model
model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),

    layers.Conv2D(32, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),

    layers.Dense(train_data.num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

print("\n=== Training Disease Prediction Model ===")

history = model.fit(
    train_data,
    validation_data=validation_data,
    epochs=EPOCHS
)

model_path = os.path.join(
    MODEL_DIR,
    "disease_prediction_model.keras"
)

model.save(model_path)

# Save class names
class_names = list(train_data.class_indices.keys())

with open(
    os.path.join(MODEL_DIR, "class_names.txt"),
    "w",
    encoding="utf-8"
) as f:
    for name in class_names:
        f.write(name + "\n")

print("\n=== Training Completed ===")
print("Model saved:", model_path)
print("Classes:", train_data.num_classes)