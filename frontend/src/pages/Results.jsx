import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const modelData = [
  { model: "Random Forest", accuracy: 99.55 },
  { model: "SVM", accuracy: 98.41 },
  { model: "Logistic Regression", accuracy: 98.41 },
  { model: "Decision Tree", accuracy: 97.95 },
  { model: "KNN", accuracy: 97.73 },
];

function Results() {
  return (
    <div className="results-page">

      {/* PAGE HEADER */}
      <section className="results-hero">
        <div className="results-hero-content">

          <span className="results-badge">
            MODEL PERFORMANCE
          </span>

          <h1>
            AgriSmart AI
            <span> Results</span>
          </h1>

          <p>
            Performance analysis of the machine learning models
            used for intelligent crop recommendation.
          </p>

        </div>
      </section>


      {/* MAIN CONTENT */}
      <main className="results-content">

        {/* SUMMARY CARDS */}
        <section className="results-summary">

          <div className="summary-card">
            <div className="summary-icon">🏆</div>

            <div>
              <span>Best Model</span>
              <h3>Random Forest</h3>
            </div>
          </div>


          <div className="summary-card">
            <div className="summary-icon">📈</div>

            <div>
              <span>Best Accuracy</span>
              <h3>99.55%</h3>
            </div>
          </div>


          <div className="summary-card">
            <div className="summary-icon">🤖</div>

            <div>
              <span>Models Tested</span>
              <h3>5 Models</h3>
            </div>
          </div>

        </section>


        {/* GRAPH */}
        <section className="results-card">

          <div className="section-heading">

            <div>
              <span className="section-label">
                PERFORMANCE ANALYSIS
              </span>

              <h2>Crop Recommendation Models</h2>

              <p>
                Accuracy comparison of the evaluated machine
                learning algorithms.
              </p>
            </div>

          </div>


          <div className="results-chart">

            <ResponsiveContainer
              width="100%"
              height={420}
            >
              <BarChart
                data={modelData}
                margin={{
                  top: 20,
                  right: 20,
                  left: 0,
                  bottom: 70,
                }}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="model"
                  angle={-15}
                  textAnchor="end"
                  interval={0}
                  height={70}
                />

                <YAxis
                  domain={[90, 100]}
                  tickFormatter={(value) =>
                    `${value}%`
                  }
                />

                <Tooltip
                  formatter={(value) => [
                    `${value}%`,
                    "Accuracy",
                  ]}
                  cursor={{ opacity: 0.08 }}
                />

                <Bar
                  dataKey="accuracy"
                  name="Accuracy"
                  radius={[8, 8, 0, 0]}
                />

              </BarChart>
            </ResponsiveContainer>

          </div>

        </section>


        {/* BEST MODEL */}
        <section className="best-model-card">

          <div className="best-model-content">

            <div className="best-model-icon">
              🏆
            </div>

            <div>
              <span className="section-label">
                SELECTED MODEL
              </span>

              <h2>Random Forest</h2>

              <p>
                Random Forest achieved the highest accuracy
                among the tested models and was selected for
                the AgriSmart AI crop recommendation system.
              </p>
            </div>

          </div>


          <div className="accuracy-box">

            <span>Accuracy</span>

            <strong>99.55%</strong>

          </div>

        </section>


        {/* MODEL TABLE */}
        <section className="results-card">

          <div className="section-heading">

            <span className="section-label">
              DETAILED RESULTS
            </span>

            <h2>Model Accuracy</h2>

            <p>
              Comparison of all evaluated crop recommendation
              models.
            </p>

          </div>


          <div className="model-table">

            <div className="model-row model-header">
              <span>Model</span>
              <span>Accuracy</span>
            </div>


            {modelData.map((item, index) => (

              <div
                className="model-row"
                key={item.model}
              >

                <div className="model-name">

                  <span className="model-rank">
                    {index + 1}
                  </span>

                  <span>{item.model}</span>

                </div>

                <strong>
                  {item.accuracy}%
                </strong>

              </div>

            ))}

          </div>

        </section>


        {/* NOTE */}
        <section className="results-note">

          <div className="note-icon">
            ℹ️
          </div>

          <div>
            <strong>About these results</strong>

            <p>
              These results are based on the evaluation of
              five machine learning algorithms using the crop
              recommendation dataset. Random Forest achieved
              the highest accuracy and was selected as the
              final crop recommendation model.
            </p>
          </div>

        </section>

      </main>

    </div>
  );
}

export default Results;