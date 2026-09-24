import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="home">

      <section className="hero">
        <div className="hero-content">
          <div className="badge">🌱 AI-Powered Agriculture</div>

          <h1>
            Smart Farming.
            <br />
            <span>Smarter Decisions.</span>
          </h1>

          <p>
            AgriSmart AI helps farmers select suitable crops based on
            environmental conditions and identify crop diseases from leaf
            images using artificial intelligence.
          </p>

          <div className="hero-buttons">
            <Link
              to="/crop-recommendation"
              className="primary-btn"
            >
              🌾 Recommend Crop
            </Link>

            <Link
              to="/disease-prediction"
              className="secondary-btn"
            >
              🍃 Detect Disease
            </Link>
          </div>
        </div>

        <div className="hero-visual">
          <div className="plant-circle">
            🌱
          </div>

          <div className="floating-card card-one">
            <span>🌾</span>
            <div>
              <strong>Crop Recommendation</strong>
              <small>AI-powered analysis</small>
            </div>
          </div>

          <div className="floating-card card-two">
            <span>🍃</span>
            <div>
              <strong>Disease Detection</strong>
              <small>Leaf image analysis</small>
            </div>
          </div>
        </div>
      </section>

      <section className="features">
        <div className="section-heading">
          <span>OUR FEATURES</span>
          <h2>Intelligence for Better Farming</h2>
          <p>
            Two intelligent modules designed to support better agricultural
            decisions.
          </p>
        </div>

        <div className="feature-grid">

          <div className="feature-card">
            <div className="feature-icon">🌾</div>
            <h3>Crop Recommendation</h3>
            <p>
              Analyze N, P, K, temperature, humidity, pH and rainfall to
              recommend a suitable crop.
            </p>
            <Link to="/crop-recommendation">
              Try Now →
            </Link>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🍃</div>
            <h3>Disease Prediction</h3>
            <p>
              Upload a crop leaf image and use AI-based image classification
              to identify possible diseases.
            </p>
            <Link to="/disease-prediction">
              Try Now →
            </Link>
          </div>

          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>Generative AI</h3>
            <p>
              Generate synthetic crop-disease images to help balance
              underrepresented disease classes.
            </p>
            <Link to="/about">
              Learn More →
            </Link>
          </div>

        </div>
      </section>

      <section className="how-section">
        <div className="section-heading">
          <span>HOW IT WORKS</span>
          <h2>From Data to Decision</h2>
        </div>

        <div className="steps">

          <div className="step">
            <div>01</div>
            <h3>Enter Data</h3>
            <p>
              Provide environmental and soil information for crop
              recommendation.
            </p>
          </div>

          <div className="step">
            <div>02</div>
            <h3>AI Analysis</h3>
            <p>
              Machine learning and deep learning models analyze the provided
              information.
            </p>
          </div>

          <div className="step">
            <div>03</div>
            <h3>Get Result</h3>
            <p>
              Receive an intelligent crop recommendation or disease
              prediction.
            </p>
          </div>

        </div>
      </section>

    </div>
  );
}

export default Home;