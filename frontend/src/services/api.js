const API_BASE_URL = "http://127.0.0.1:5000/api";

// Check backend
export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend is unavailable");
  }

  return response.json();
};


// Crop Recommendation
export const recommendCrop = async (cropData) => {
  const response = await fetch(
    `${API_BASE_URL}/crop-recommendation`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(cropData),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Crop recommendation failed"
    );
  }

  return data;
};


// Disease Prediction
export const predictDisease = async (imageFile) => {
  const formData = new FormData();

  formData.append("image", imageFile);

  const response = await fetch(
    `${API_BASE_URL}/disease-prediction`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Disease prediction failed"
    );
  }

  return data;
};