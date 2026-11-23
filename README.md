# AgriSmart

Flask API for crop recommendation (Random Forest) and plant disease prediction (MobileNetV2), plus a frontend in `frontend/`.

## Run the backend
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r backend/requirements.txt
    python backend/app.py

The API runs on http://localhost:5000
- POST /api/crop-recommend  (JSON: N, P, K, temperature, humidity, ph, rainfall)
- POST /api/disease-predict (multipart form field: image)

## Notes
- Trained models are included in the repo (no Git LFS needed).
- The PlantVillage training dataset is not included; it is only needed to retrain.
- Frontend: see the scripts in frontend/package.json.
