import { NavLink, Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-container">

        {/* Brand */}
        <Link to="/" className="brand">
          <div className="brand-symbol">
            <span>⌁</span>
          </div>

          <div className="brand-name">
            AgriSmart
            <span>AI</span>
          </div>
        </Link>


        {/* Navigation */}
        <nav className="nav-links">

          <NavLink to="/" end>
            Home
          </NavLink>

          <NavLink to="/crop-recommendation">
            Crop Recommendation
          </NavLink>

          <NavLink to="/disease-prediction">
            Disease Prediction
          </NavLink>

          <NavLink to="/results">
            Results
          </NavLink>

          <NavLink to="/about">
            About
          </NavLink>

        </nav>


        {/* CTA */}
        <Link
          to="/crop-recommendation"
          className="nav-cta"
        >
          Get Started
          <span>↗</span>
        </Link>

      </div>
    </header>
  );
}

export default Navbar;