import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import CropRecommendation from "./pages/CropRecommendation";
import DiseasePrediction from "./pages/DiseasePrediction";
import Results from "./pages/Results";
import About from "./pages/About";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">

        <Navbar />

        <main>
          <Routes>

            {/* Home */}
            <Route path="/" element={<Home />} />

            {/* Crop Recommendation */}
            <Route
              path="/crop-recommendation"
              element={<CropRecommendation />}
            />

            {/* Disease Prediction */}
            <Route
              path="/disease-prediction"
              element={<DiseasePrediction />}
            />

            {/* Results & Graphs */}
            <Route
              path="/results"
              element={<Results />}
            />

            {/* About */}
            <Route
              path="/about"
              element={<About />}
            />

            {/* Invalid URL */}
            <Route
              path="*"
              element={<Navigate to="/" replace />}
            />

          </Routes>
        </main>

        <Footer />

      </div>
    </BrowserRouter>
  );
}

export default App;