from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)


# ========================================================
# CROP RECOMMENDATION MODEL
# ========================================================

CROP_MODEL_PATH = os.path.join(
    "..",
    "models",
    "crop_recommendation",
    "best_crop_model.pkl"
)

with open(CROP_MODEL_PATH, "rb") as file:
    crop_model = pickle.load(file)

print("Crop recommendation model loaded successfully!")


# ========================================================
# DISEASE MODEL
# ========================================================

DISEASE_MODEL_PATH = os.path.join(
    "..",
    "models",
    "disease_prediction",
    "disease_prediction_model.keras"
)

DISEASE_CLASS_PATH = os.path.join(
    "..",
    "models",
    "disease_prediction",
    "class_names.txt"
)

DISEASE_CLASS_PATH = os.path.join(
    "models",
    "disease_prediction",
    "class_names.txt"
)

disease_model = None
disease_classes = []


# Load disease model only if it exists
if os.path.exists(DISEASE_MODEL_PATH):

    try:
        import tensorflow as tf

        disease_model = tf.keras.models.load_model(
            DISEASE_MODEL_PATH
        )

        print("Disease prediction model loaded successfully!")

    except Exception as e:

        print(
            "Disease model found but could not be loaded:",
            e
        )

else:

    print(
        "Disease prediction model not available yet."
    )


# Load disease class names
if os.path.exists(DISEASE_CLASS_PATH):

    with open(
        DISEASE_CLASS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        disease_classes = [
            line.strip()
            for line in file
            if line.strip()
        ]

    print(
        f"Disease classes loaded: {len(disease_classes)}"
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "message": "AgriSmart AI Backend is running"
    })


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    return jsonify({
        "status": "OK"
    })


# =========================================================
# CROP RECOMMENDATION
# =========================================================

@app.route(
    "/api/crop-recommendation",
    methods=["POST"]
)
def crop_recommendation():

    try:

        data = request.get_json()

        required_fields = [
            "N",
            "P",
            "K",
            "temperature",
            "humidity",
            "ph",
            "rainfall"
        ]

        for field in required_fields:

            if field not in data:

                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400

        N = float(data["N"])
        P = float(data["P"])
        K = float(data["K"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["ph"])
        rainfall = float(data["rainfall"])

        input_data = np.array([[
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        ]])

        prediction = crop_model.predict(
            input_data
        )

        recommended_crop = prediction[0]

        return jsonify({
            "success": True,
            "recommended_crop": str(
                recommended_crop
            )
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# =========================================================
# DISEASE PREDICTION
# =========================================================

@app.route(
    "/api/disease-prediction",
    methods=["POST"]
)
def disease_prediction():

    try:

        # Check whether model is available
        if disease_model is None:

            return jsonify({
                "success": False,
                "error": (
                    "Disease prediction model is not "
                    "trained yet."
                )
            }), 503


        # Check image
        if "image" not in request.files:

            return jsonify({
                "success": False,
                "error": "No image uploaded."
            }), 400


        image_file = request.files["image"]


        if image_file.filename == "":

            return jsonify({
                "success": False,
                "error": "No image selected."
            }), 400


        # Import image utilities
        from PIL import Image


        # Open uploaded image
        image = Image.open(
            image_file
        ).convert("RGB")


        # Resize
        image = image.resize(
            (224, 224)
        )


        # Convert image to numpy
        image_array = np.array(
            image,
            dtype=np.float32
        )


        # Normalize
        image_array = image_array / 255.0


        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # Prediction
        predictions = disease_model.predict(
            image_array,
            verbose=0
        )


        predicted_index = int(
            np.argmax(predictions[0])
        )


        confidence = float(
            predictions[0][predicted_index] * 100
        )


        # Get disease name
        if (
            predicted_index
            < len(disease_classes)
        ):

            disease_name = disease_classes[
                predicted_index
            ]

        else:

            disease_name = (
                "Unknown disease"
            )


        return jsonify({

            "success": True,

            "disease": disease_name,

            "confidence": round(
                confidence,
                2
            ),

            "symptoms": (
                "Disease symptoms will be "
                "provided here."
            ),

            "prevention": (
                "Prevention information will "
                "be provided here."
            ),

            "management": (
                "Basic management information "
                "will be provided here."
            )

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )
