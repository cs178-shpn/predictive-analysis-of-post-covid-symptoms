from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model, scaler, and feature names
rf_model = joblib.load("random_forest_model.pkl")
scaler = joblib.load("feature_scaler.pkl")
features = joblib.load("feature_names.pkl")

def preprocess_input(data):
    """Convert input data to model-compatible format."""
    input_array = []
    for feature in features:
        # Handle one-hot encoded features
        if feature.startswith(('gender_', 'severity_')):
            input_array.append(data.get(feature, 0))
        else:
            input_array.append(data.get(feature, 0))
    
    # Scale the features
    return scaler.transform([input_array])[0]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json

        # Validate input
        required_features = [
            'age', 'diabetes', 'hypertension', 
            'fatigue', 'breathlessness', 
            'brain_fog', 'joint_pain',
            'gender_Male', 'severity_Moderate', 'severity_Severe'
        ]
        for feature in required_features:
            if feature not in data:
                return jsonify({"error": f"Missing required feature: {feature}"}), 400

        # Preprocess the input
        input_scaled = preprocess_input(data)

        # Predict probabilities using the Random Forest model
        probabilities = rf_model.predict_proba(input_scaled.reshape(1, -1))[0]

        # Define specific symptoms and their probabilities
        fatigue_prob = probabilities[1] * 80  # Example scaling
        breathlessness_prob = probabilities[1] * 50  # Example scaling
        brain_fog_prob = probabilities[1] * 30  # Example scaling

        # Construct the response
        response = {
            "predictions": {
                "fatigue": f"{round(fatigue_prob, 2)}% chance of long-term fatigue.",
                "breathlessness": f"{round(breathlessness_prob, 2)}% chance of breathlessness.",
                "brain_fog": f"{round(brain_fog_prob,2)}% chance of brain fog."
            },
            "disclaimer": "disclaimer:This is a predictive tool and not a medical diagnosis. Always consult healthcare professionals."
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Post-COVID Symptom Predictor",
        "version": "1.0.0",
        "status": "operational"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
