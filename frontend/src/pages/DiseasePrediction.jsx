import { useState } from "react";

function DiseasePrediction() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleFile = (selectedFile) => {
    if (!selectedFile) return;

    const allowed = [
      "image/jpeg",
      "image/jpg",
      "image/png",
    ];

    if (!allowed.includes(selectedFile.type)) {
      setError("Please upload a JPG, JPEG or PNG image.");
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null);
    setError("");
  };

  const handleChange = (e) => {
    handleFile(e.target.files[0]);
  };

  const removeImage = () => {
    setFile(null);
    setPreview("");
    setResult(null);
    setError("");
  };

  const predictDisease = async () => {
    if (!file) {
      setError("Please upload a leaf image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("image", file);

      const response = await fetch(
        "http://127.0.0.1:5000/api/disease-prediction",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error();
      }

      const data = await response.json();
      setResult(data);
    } catch {
      setError(
        "Disease prediction service is currently unavailable."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-container">

      <div className="page-header">
        <span>🍃 DISEASE PREDICTION</span>
        <h1>Detect Crop Disease</h1>
        <p>
          Upload a crop leaf image and let the AI model analyze it.
        </p>
      </div>

      <div className="disease-layout">

        <div className="upload-card">

          <h2>Upload Leaf Image</h2>

          {!preview ? (
            <label className="upload-area">
              <div className="upload-icon">📷</div>

              <h3>Upload your leaf image</h3>

              <p>
                Drag and drop or click to select
              </p>

              <span>
                JPG, JPEG or PNG
              </span>

              <input
                type="file"
                accept=".jpg,.jpeg,.png"
                onChange={handleChange}
              />
            </label>
          ) : (
            <div className="preview-container">

              <img
                src={preview}
                alt="Selected crop leaf"
              />

              <button
                className="remove-btn"
                onClick={removeImage}
              >
                Remove Image
              </button>

            </div>
          )}

          {error && (
            <div className="error-message">
              ⚠️ {error}
            </div>
          )}

          <button
            className="primary-btn predict-btn"
            onClick={predictDisease}
            disabled={!file || loading}
          >
            {loading ? "Analyzing Image..." : "🔍 Predict Disease"}
          </button>

        </div>

        <div className="disease-result">

          {!result && !loading && (
            <div className="empty-result">
              <div className="result-icon">🍃</div>
              <h2>Disease Result</h2>
              <p>
                Upload a leaf image to see the prediction.
              </p>
            </div>
          )}

          {loading && (
            <div className="empty-result">
              <div className="loader"></div>
              <h2>Analyzing Image...</h2>
              <p>
                Please wait while the AI model processes your image.
              </p>
            </div>
          )}

          {result && (
            <div className="disease-success">

              <span>PREDICTED DISEASE</span>

              <h2>
                {result.disease ||
                  result.predicted_disease ||
                  result.prediction}
              </h2>

              {result.confidence && (
                <div className="confidence">
                  Confidence: {Number(result.confidence).toFixed(2)}%
                </div>
              )}

              {result.symptoms && (
                <div className="info-section">
                  <h3>Symptoms</h3>
                  <p>{result.symptoms}</p>
                </div>
              )}

              {result.prevention && (
                <div className="info-section">
                  <h3>Prevention</h3>
                  <p>{result.prevention}</p>
                </div>
              )}

              {result.management && (
                <div className="info-section">
                  <h3>Management</h3>
                  <p>{result.management}</p>
                </div>
              )}

            </div>
          )}

        </div>

      </div>
    </div>
  );
}

export default DiseasePrediction;