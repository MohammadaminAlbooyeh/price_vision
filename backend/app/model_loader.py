import joblib
import os

def load_model():
    """Load trained models and features from the models directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_sale_path = os.path.join(base_dir, "models", "model_sale.pkl")
    model_rent_path = os.path.join(base_dir, "models", "model_rent.pkl")
    features_path = os.path.join(base_dir, "models", "features.pkl")

    if not os.path.exists(features_path):
        raise FileNotFoundError(f"features.pkl missing in {os.path.join(base_dir, 'models')}")

    features = joblib.load(features_path)
    models = {}

    if os.path.exists(model_sale_path):
        models['sale'] = joblib.load(model_sale_path)
    if os.path.exists(model_rent_path):
        models['rent'] = joblib.load(model_rent_path)

    if not models:
        raise FileNotFoundError(f"No models found in {os.path.join(base_dir, 'models')}")

    return models, features
