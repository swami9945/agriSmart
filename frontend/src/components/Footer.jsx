import { Link } from "react-router-dom";

function Footer() {
  return (
    <footer className="footer">

      <div className="footer-main">

        {/* Brand section */}
        <div className="footer-intro">

          <Link to="/" className="footer-brand">
            <div className="footer-symbol">
              ⌁
            </div>

            <div>
              <strong>AgriSmart AI</strong>
              <span>Intelligent Agriculture</span>
            </div>
          </Link>

          <p>
            Intelligent crop recommendation and plant disease
            prediction powered by machine learning, deep learning
            and generative AI.
          </p>

        </div>


        {/* Navigation */}
        <div className="footer-links">

          <div className="footer-group">
            <h4>Platform</h4>

            <Link to="/crop-recommendation">
              Crop Recommendation
            </Link>

            <Link to="/disease-prediction">
              Disease Prediction
            </Link>

            <Link to="/results">
              Model Results
            </Link>
          </div>


          <div className="footer-group">
            <h4>Project</h4>

            <Link to="/">Home</Link>

            <Link to="/about">
              About AgriSmart
            </Link>

            <Link to="/results">
              Performance
            </Link>
          </div>


          <div className="footer-group">
            <h4>Technology</h4>

            <span>Machine Learning</span>
            <span>Deep Learning</span>
            <span>Generative AI</span>
            <span>React & Python</span>
          </div>

        </div>

      </div>


      {/* Bottom */}
      <div className="footer-bottom">

        <span>
          © {new Date().getFullYear()} AgriSmart AI
        </span>

        <span>
          Intelligent technology for smarter agriculture
        </span>

      </div>

    </footer>
  );
}

export default Footer;