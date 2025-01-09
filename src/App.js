import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [formData, setFormData] = useState({
    age: "",
    diabetes: 0,
    hypertension: 0,
    fatigue: 0,
    breathlessness: 0,
    brain_fog: 0,
    joint_pain: 0,
    gender_Male: 1,
    severity_Moderate: 0,
    severity_Severe: 0,
  });

  const [name, setName] = useState(""); // New state for name
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "age" ? parseInt(value) : parseInt(value),
    }));
  };

  const handleSeverity = (severity) => {
    setFormData((prev) => ({
      ...prev,
      severity_Moderate: severity === "moderate" ? 1 : 0,
      severity_Severe: severity === "severe" ? 1 : 0,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPrediction(null);

    try {
      const response = await axios.post("http://localhost:5000/predict", formData);
      setPrediction(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-md mx-auto bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center">
          Post-COVID Symptom Risk Predictor
        </h1>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* New name input field */}
          <div>
            <label className="block mb-2">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your name"
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block mb-2">Age</label>
            <input
              type="number"
              name="age"
              value={formData.age}
              onChange={handleChange}
              placeholder="Enter your age"
              required
              className="w-full p-2 border rounded"
            />
          </div>

          {/* Rest of the code remains the same */}
          {["diabetes", "hypertension", "fatigue", "breathlessness", "brain_fog", "joint_pain"].map((field) => (
            <div key={field}>
              <label className="block mb-2">{field.replace("_", " ").replace(/\b\w/g, (l) => l.toUpperCase())}</label>
              <select
                name={field}
                value={formData[field]}
                onChange={handleChange}
                className="w-full p-2 border rounded"
              >
                <option value={0}>No</option>
                <option value={1}>Yes</option>
              </select>
            </div>
          ))}

          <div>
            <label className="block mb-2">Gender</label>
            <select
              name="gender_Male"
              value={formData.gender_Male}
              onChange={handleChange}
              className="w-full p-2 border rounded"
            >
              <option value={1}>Male</option>
              <option value={0}>Female</option>
            </select>
          </div>

          <div>
            <label className="block mb-2">COVID Severity</label>
            <div className="flex space-x-2">
              <button
                type="button"
                onClick={() => handleSeverity("mild")}
                className={`flex-1 p-2 rounded ${
                  formData.severity_Moderate === 0 && formData.severity_Severe === 0
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200"
                }`}
              >
                Mild
              </button>
              <button
                type="button"
                onClick={() => handleSeverity("moderate")}
                className={`flex-1 p-2 rounded ${
                  formData.severity_Moderate === 1 ? "bg-blue-500 text-white" : "bg-gray-200"
                }`}
              >
                Moderate
              </button>
              <button
                type="button"
                onClick={() => handleSeverity("severe")}
                className={`flex-1 p-2 rounded ${
                  formData.severity_Severe === 1 ? "bg-blue-500 text-white" : "bg-gray-200"
                }`}
              >
                Severe
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full p-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            {loading ? "Predicting..." : "Predict Risk"}
          </button>
        </form>

        {error && (
          <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">
            {error}
          </div>
        )}

        {prediction && (
          <div className="mt-6 p-4 bg-blue-100 rounded">
            <h2 className="text-xl font-bold mb-4">Prediction Results of {name}</h2>
            <div className="space-y-2">
              <p>{prediction.predictions.fatigue}</p>
              <p>{prediction.predictions.breathlessness}</p>
              <p>{prediction.predictions.brain_fog}</p>
            </div>
            <br/>
            <br/>
            <p className="mt-4 text-sm text-gray-600">
              {prediction.disclaimer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;