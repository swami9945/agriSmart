import torch
import torch.nn as nn
import pickle

from torchvision import models
from PIL import Image

from disease_prediction.utils.preprocess import preprocess_image


# ==========================================
# 1. CONFIGURATION
# ==========================================

MODEL_PATH = "backend/disease_prediction/models/MobileNetV2_Download/mobilenetv2.pth"

CLASS_PATH = "backend/disease_prediction/models/MobileNetV2_Download/class_names.pkl"

IMAGE_PATH = "test_images/tomato_test.jpg"

DEVICE = torch.device("cpu")


# ==========================================
# 2. LOAD CHECKPOINT
# ==========================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE,
    weights_only=False
)


# ==========================================
# 3. RECONSTRUCT MODEL
# ==========================================

model = models.mobilenet_v2(weights=None)

model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    checkpoint["num_classes"]
)

model.load_state_dict(checkpoint["model_state_dict"])

model.to(DEVICE)
model.eval()


# ==========================================
# 4. LOAD CLASS NAMES
# ==========================================

with open(CLASS_PATH, "rb") as f:
    class_names = pickle.load(f)


# ==========================================
# 5. PREPROCESS IMAGE
# ==========================================

image_tensor = preprocess_image(
    IMAGE_PATH,
    image_size=224
)

image_tensor = image_tensor.to(DEVICE)


# ==========================================
# 6. PREDICTION
# ==========================================

with torch.no_grad():

    outputs = model(image_tensor)

    probabilities = torch.softmax(outputs, dim=1)

    confidence, predicted_index = torch.max(
        probabilities,
        dim=1
    )


# ==========================================
# 7. DISPLAY RESULT
# ==========================================

predicted_disease = class_names[predicted_index.item()]

confidence_percentage = confidence.item() * 100

print("\n===================================")
print("AGRISMART AI - DISEASE PREDICTION")
print("===================================")

print("Model: MobileNetV2")

print("Predicted Disease:", predicted_disease)

print("Confidence: {:.2f}%".format(confidence_percentage))

print("===================================")