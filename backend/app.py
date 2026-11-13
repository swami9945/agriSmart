from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import os
import torch
import torch.nn as nn
import pickle
import tempfile

from torchvision import models
from disease_prediction.utils.preprocess import preprocess_image


# ==========================================
# 1. FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)
CORS(app)

DEVICE = torch.device("cpu")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ==========================================
# 2. LOAD RANDOM FOREST MODEL
# ==========================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "crop_recommendation",
    "models",
    "random_forest.joblib"
)

model = joblib.load(MODEL_PATH)

print("Random Forest model loaded successfully!")


# ==========================================
# 3. LOAD MOBILENETV2 MODEL
# ==========================================

DISEASE_MODEL_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "disease_prediction",
    "models",
    "MobileNetV2_Download",
    "mobilenetv2.pth"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "disease_prediction",
    "models",
    "MobileNetV2_Download",
    "class_names.pkl"
)


checkpoint = torch.load(
    DISEASE_MODEL_PATH,
    map_location=DEVICE,
    weights_only=False
)

disease_model = models.mobilenet_v2(weights=None)

disease_model.classifier[1] = nn.Linear(
    disease_model.classifier[1].in_features,
    checkpoint["num_classes"]
)

disease_model.load_state_dict(
    checkpoint["model_state_dict"],
    strict=True
)

disease_model.to(DEVICE)
disease_model.eval()


# Load trained class names

with open(CLASS_PATH, "rb") as f:
    disease_class_names = pickle.load(f)


print("MobileNetV2 loaded successfully!")
print("Number of disease classes:", len(disease_class_names))


# ==========================================
# 4. CROP RECOMMENDATION API
# ==========================================

@app.route("/api/crop-recommend", methods=["POST"])
def crop_recommend():

    try:

        data = request.get_json()

        N = float(data["N"])
        P = float(data["P"])
        K = float(data["K"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["ph"])
        rainfall = float(data["rainfall"])

        features = [[
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        ]]

        prediction = model.predict(features)

        return jsonify({
            "success": True,
            "recommended_crop": prediction[0]
        })

    except KeyError as e:

        return jsonify({
            "success": False,
            "error": f"Missing input field: {str(e)}"
        }), 400

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ==========================================
# 5. DISEASE PREDICTION API
# ==========================================

@app.route("/api/disease-predict", methods=["POST"])
def disease_predict():

    temp_path = None

    try:

        # Receive uploaded image

        if "image" not in request.files:

            return jsonify({
                "success": False,
                "error": "Please upload a plant leaf image."
            }), 400

        image_file = request.files["image"]

        if image_file.filename == "":

            return jsonify({
                "success": False,
                "error": "No image selected."
            }), 400

        # Save temporary image

        with tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        ) as temp:

            image_file.save(temp.name)
            temp_path = temp.name

        # Preprocess image

        image_tensor = preprocess_image(
            temp_path,
            image_size=224
        )

        image_tensor = image_tensor.to(DEVICE)

        # Predict disease

        with torch.no_grad():

            outputs = disease_model(image_tensor)

            probabilities = torch.softmax(outputs, dim=1)

            confidence, predicted_index = torch.max(
                probabilities,
                dim=1
            )

        # Get predicted class

        predicted_disease = disease_class_names[
            predicted_index.item()
        ]

        confidence_percentage = confidence.item() * 100

        # Return result

        return jsonify({

            "success": True,

            "model": "MobileNetV2",

            "predicted_disease": predicted_disease,

            "confidence": round(confidence_percentage, 2)

        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ==========================================
# 6. HOME API
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "message": "AgriSmart AI API is running",

        "crop_recommendation": True,

        "disease_prediction": True

    })


# ==========================================
# 7. RUN FLASK
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )