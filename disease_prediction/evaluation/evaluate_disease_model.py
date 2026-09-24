import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

MODEL_PATH = "models/disease_prediction/disease_prediction_model.keras"
DATASET_DIR = "datasets/crop_disease/raw/balanced"
RESULTS_DIR = "results/disease_prediction"

os.makedirs(RESULTS_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

model = tf.keras.models.load_model(MODEL_PATH)

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2
)

test_data = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

loss, accuracy = model.evaluate(test_data)

print("\n=== Disease Model Evaluation ===")
print(f"Loss     : {loss:.4f}")
print(f"Accuracy : {accuracy:.4f}")

predictions = model.predict(test_data)
y_pred = np.argmax(predictions, axis=1)
y_true = test_data.classes

class_names = list(test_data.class_indices.keys())

report = classification_report(
    y_true,
    y_pred,
    target_names=class_names
)

print("\n=== Classification Report ===")
print(report)

with open(
    os.path.join(RESULTS_DIR, "classification_report.txt"),
    "w",
    encoding="utf-8"
) as f:
    f.write(report)

cm = confusion_matrix(y_true, y_pred)

np.savetxt(
    os.path.join(RESULTS_DIR, "confusion_matrix.csv"),
    cm,
    delimiter=",",
    fmt="%d"
)

print("\nEvaluation completed!")