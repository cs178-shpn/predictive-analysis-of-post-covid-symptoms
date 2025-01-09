import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

# Ensure the post_covid/src directory exists
src_dir = "post_covid/src"
if not os.path.exists(src_dir):
    os.makedirs(src_dir)

# Improved synthetic data generation
def generate_synthetic_data(n_samples=2000):
    np.random.seed(42)
    age = np.random.normal(45, 15, n_samples).clip(18, 85)
    gender = np.random.choice(["Male", "Female"], n_samples)
    diabetes = (np.random.random(n_samples) < 0.2).astype(int)
    hypertension = (np.random.random(n_samples) < 0.3).astype(int)

    # Generate probabilities for symptoms
    fatigue_prob = 0.3 + 0.1 * (age > 50) + 0.2 * diabetes
    fatigue = (np.random.random(n_samples) < fatigue_prob).astype(int)

    breathlessness_prob = 0.2 + 0.1 * (age > 60) + 0.2 * hypertension
    breathlessness = (np.random.random(n_samples) < breathlessness_prob).astype(int)

    brain_fog_prob = 0.1 + 0.15 * (age > 55)
    brain_fog = (np.random.random(n_samples) < brain_fog_prob).astype(int)

    # Long COVID target
    long_covid = (fatigue + breathlessness + brain_fog > 1).astype(int)

    data = {
        "age": age,
        "gender": gender,
        "diabetes": diabetes,
        "hypertension": hypertension,
        "fatigue": fatigue,
        "breathlessness": breathlessness,
        "brain_fog": brain_fog,
        "long_covid": long_covid,
    }
    return pd.DataFrame(data)

# Generate and save the dataset
df = generate_synthetic_data()
dataset_path = os.path.join(src_dir, "synthetic_covid_data.csv")
df.to_csv(dataset_path, index=False)
print(f"Synthetic dataset saved at: {dataset_path}")

# Encode categorical variables
df_encoded = pd.get_dummies(df, columns=["gender"], drop_first=True)

# Separate features and targets
X = df_encoded.drop(["fatigue", "breathlessness", "brain_fog"], axis=1)
y = df_encoded[["fatigue", "breathlessness", "brain_fog"]]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a single Random Forest model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_model.predict(X_test)
print("Classification Report (Fatigue):")
print(classification_report(y_test["fatigue"], y_pred[:, 0]))
print("Classification Report (Breathlessness):")
print(classification_report(y_test["breathlessness"], y_pred[:, 1]))
print("Classification Report (Brain Fog):")
print(classification_report(y_test["brain_fog"], y_pred[:, 2]))

# Save the model and preprocessing artifacts
joblib.dump(rf_model, os.path.join(src_dir, "random_forest_model.pkl"))
joblib.dump(scaler, os.path.join(src_dir, "feature_scaler.pkl"))
joblib.dump(X.columns.tolist(), os.path.join(src_dir, "feature_names.pkl"))

print("Model and artifacts saved successfully in 'post_covid/src'!")
