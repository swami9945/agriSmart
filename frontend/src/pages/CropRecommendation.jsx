import { useState } from "react";
import { recommendCrop } from "../services/api";

function CropRecommendation() {
  const [form, setForm] = useState({
    N: "",
    P: "",
    K: "",
    temperature: "",
    humidity: "",
    ph: "",
    rainfall: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setResult(null);

    // Check all fields
    const values = Object.values(form);

    if (values.some((value) => value === "")) {
      setError("Please fill in all fields.");
      return;
    }

    setLoading(true);

    try {
      // Send data to Flask through api.js
      const data = await recommendCrop({
        N: Number(form.N),
        P: Number(form.P),
        K: Number(form.K),
        temperature: Number(form.temperature),
        humidity: Number(form.humidity),
        ph: Number(form.ph),
        rainfall: Number(form.rainfall),
      });

      setResult(data);
    } catch (error) {
      setError(
        error.message ||
          "Crop recommendation service is currently unavailable."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setForm({
      N: "",
      P: "",
      K: "",
      temperature: "",
      humidity: "",
      ph: "",
      rainfall: "",
    });

    setResult(null);
    setError("");
  };

  return (
    <div className="page-container">

      {/* PAGE HEADER */}
      <div className="page-header">
        <span>🌾 CROP RECOMMENDATION</span>

        <h1>Find the Right Crop</h1>

        <p>
          Enter your soil and environmental conditions to get an
          AI-powered crop recommendation.
        </p>
      </div>


      {/* MAIN CONTENT */}
      <div className="recommendation-layout">

        {/* FORM CARD */}
        <div className="form-card">

          <h2>Environmental Conditions</h2>

          <p className="form-description">
            Enter the values from your field.
          </p>


          <form onSubmit={handleSubmit}>

            <div className="input-grid">

              {/* Nitrogen */}
              <div className="input-group">
                <label>Nitrogen (N)</label>

                <input
                  type="number"
                  step="any"
                  name="N"
                  value={form.N}
                  onChange={handleChange}
                  placeholder="Example: 90"
                />
              </div>


              {/* Phosphorus */}
              <div className="input-group">
                <label>Phosphorus (P)</label>

                <input
                  type="number"
                  step="any"
                  name="P"
                  value={form.P}
                  onChange={handleChange}
                  placeholder="Example: 42"
                />
              </div>


              {/* Potassium */}
              <div className="input-group">
                <label>Potassium (K)</label>

                <input
                  type="number"
                  step="any"
                  name="K"
                  value={form.K}
                  onChange={handleChange}
                  placeholder="Example: 43"
                />
              </div>


              {/* Temperature */}
              <div className="input-group">
                <label>Temperature (°C)</label>

                <input
                  type="number"
                  step="any"
                  name="temperature"
                  value={form.temperature}
                  onChange={handleChange}
                  placeholder="Example: 25"
                />
              </div>


              {/* Humidity */}
              <div className="input-group">
                <label>Humidity (%)</label>

                <input
                  type="number"
                  step="any"
                  name="humidity"
                  value={form.humidity}
                  onChange={handleChange}
                  placeholder="Example: 80"
                />
              </div>


              {/* pH */}
              <div className="input-group">
                <label>pH</label>

                <input
                  type="number"
                  step="any"
                  name="ph"
                  value={form.ph}
                  onChange={handleChange}
                  placeholder="Example: 6.5"
                />
              </div>


              {/* Rainfall */}
              <div className="input-group full">
                <label>Rainfall (mm)</label>

                <input
                  type="number"
                  step="any"
                  name="rainfall"
                  value={form.rainfall}
                  onChange={handleChange}
                  placeholder="Example: 200"
                />
              </div>

            </div>


            {/* ERROR */}
            {error && (
              <div className="error-message">
                ⚠️ {error}
              </div>
            )}


            {/* BUTTONS */}
            <div className="form-buttons">

              <button
                type="submit"
                className="primary-btn"
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : "🌱 Get Recommendation"}
              </button>


              <button
                type="button"
                className="reset-btn"
                onClick={resetForm}
              >
                Reset
              </button>

            </div>

          </form>

        </div>


        {/* RESULT CARD */}
        <div className="result-card">

          {/* EMPTY */}
          {!result && !loading && (
            <div className="empty-result">

              <div className="result-icon">
                🌾
              </div>

              <h2>Your Result</h2>

              <p>
                Enter your field conditions and click
                <strong> Get Recommendation</strong>.
              </p>

            </div>
          )}


          {/* LOADING */}
          {loading && (
            <div className="empty-result">

              <div className="loader"></div>

              <h2>Analyzing...</h2>

              <p>
                Our AI model is analyzing your field
                conditions.
              </p>

            </div>
          )}


          {/* RESULT */}
          {result && (
            <div className="success-result">

              <div className="result-icon">
                🌱
              </div>

              <span>
                RECOMMENDED CROP
              </span>

              <h2>
                {result.recommended_crop ||
                  result.crop ||
                  result.prediction}
              </h2>

              <p>
                Based on the environmental and soil
                conditions you provided.
              </p>

            </div>
          )}

        </div>

      </div>

    </div>
  );
}

export default CropRecommendation;