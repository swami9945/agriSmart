from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os

app = Flask(__name__)
CORS(app)

# Path to the trained Random Forest model
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "ml",
    "crop_recommendation",
    "models",
    "random_forest.joblib"
)

# Load trained model
model = joblib.load(MODEL_PATH)

print("Random Forest model loaded successfully!")


@app.route("/api/crop-recommend", methods=["POST"])
def crop_recommend():
    try:
        data = request.get_json()

        # Get input values
        N = float(data["N"])
        P = float(data["P"])
        K = float(data["K"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        ph = float(data["ph"])
        rainfall = float(data["rainfall"])

        # Keep the same feature order used during training
        features = [[
            N,
            P,
            K,
            temperature,
            humidity,
            ph,
            rainfall
        ]]

        # Predict crop
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


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AgriSmart Crop Recommendation API is running"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)