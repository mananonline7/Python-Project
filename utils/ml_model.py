from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "random_forest_model.pkl"

model = joblib.load(MODEL_PATH)


def predict_fault(mean, peak, peak_to_peak, rms, std):

    features = pd.DataFrame([{
        "Mean": mean,
        "Peak": peak,
        "Peak_to_Peak": peak_to_peak,
        "RMS": rms,
        "Std": std
    }])
   
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max() * 100

    label_mapping = {
    0: "Healthy",
    1: "Inner Race Fault",
    2: "Ball Fault",
    3: "Outer Race Fault"
    }

    prediction_name = label_mapping.get(
    int(prediction),
    "Unknown"
    )

    return prediction_name, confidence