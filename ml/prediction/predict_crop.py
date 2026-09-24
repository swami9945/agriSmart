import os
import pandas as pd
import joblib


MODEL_FILE = "models/crop_recommendation/best_crop_model.pkl"
LABEL_FILE = "datasets/crop_recommendation/processed/label_mapping.csv"


# Load model
model = joblib.load(MODEL_FILE)

# Load label mapping
label_mapping = pd.read_csv(LABEL_FILE)

label_dict = dict(
    zip(
        label_mapping["encoded_label"],
        label_mapping["crop"]
    )
)


def predict_crop(N, P, K, temperature, humidity, ph, rainfall):

    input_data = pd.DataFrame([{
        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall
    }])

    prediction = model.predict(input_data)[0]

    crop = label_dict[prediction]

    return crop


if __name__ == "__main__":

    # Sample input
    N = 90
    P = 42
    K = 43
    temperature = 20.8
    humidity = 82.0
    ph = 6.5
    rainfall = 202.9

    crop = predict_crop(
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    )

    print("=== Crop Recommendation ===")
    print("Recommended Crop:", crop)