function About() {
  return (
    <div className="page-container">

      <div className="page-header">
        <span>ABOUT AGRISMART AI</span>
        <h1>Technology for Smarter Agriculture</h1>
        <p>
          An intelligent system combining machine learning, deep learning
          and generative AI.
        </p>
      </div>

      <section className="about-content">

        <div className="about-card">
          <div className="about-icon">🌱</div>

          <h2>What is AgriSmart AI?</h2>

          <p>
            AgriSmart AI is an intelligent agricultural system designed to
            support farmers with crop selection and crop disease prediction.
          </p>

          <p>
            The system analyzes soil and environmental conditions to recommend
            suitable crops. It also analyzes crop leaf images to identify
            possible diseases.
          </p>
        </div>

        <div className="about-card">
          <div className="about-icon">🤖</div>

          <h2>Generative AI</h2>

          <p>
            Generative AI is used to create synthetic crop-disease images for
            underrepresented classes. These images help balance the disease
            dataset and improve the robustness of disease prediction.
          </p>
        </div>

      </section>

      <section className="technology-section">

        <div className="section-heading">
          <span>TECHNOLOGY STACK</span>
          <h2>Built With</h2>
        </div>

        <div className="technology-grid">

          <div>⚛️ React</div>
          <div>🐍 Python</div>
          <div>🌐 Flask</div>
          <div>🧠 Machine Learning</div>
          <div>🔬 Deep Learning</div>
          <div>🤖 Generative AI</div>

        </div>

      </section>

    </div>
  );
}

export default About;