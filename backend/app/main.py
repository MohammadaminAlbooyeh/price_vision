from fastapi import FastAPI, HTTPException
from .model_loader import load_model
from .schemas import PredictionRequest, PredictionResponse
from fastapi.responses import JSONResponse
from .logger import logger
import pandas as pd
import sys
import os
from fastapi.middleware.cors import CORSMiddleware

# Align with training feature engineering
# Add src to path to reuse feature engineering logic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.feature_engineering import feature_engineering

app = FastAPI(title="PriceVision API")

# Enable CORS for frontend development (allow current Vite ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load the models and expected features
try:
    models, features_list = load_model()
    logger.info("Model(s) and feature list loaded successfully")
    logger.info(f"Loaded models: {list(models.keys())}")
    logger.info(f"Loaded features list: {features_list}")
except Exception as e:
    logger.error(f"Error loading model artifacts: {e}")
    models, features_list = {}, None

@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    return {"message": "Welcome to PriceVision API"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    logger.info(f"Predict request: {request}")
    if not models or features_list is None:
        logger.error("Predict endpoint called but model artifacts not loaded")
        raise HTTPException(status_code=500, detail="Machine Learning model not loaded on server.")

    if request.mode not in {"sale", "rent"}:
        raise HTTPException(status_code=400, detail="mode must be 'sale' or 'rent'")

    if request.mode not in models:
        raise HTTPException(status_code=500, detail=f"No model available for mode '{request.mode}'")

    try:
        input_dict = request.model_dump(by_alias=True)
        df_input = pd.DataFrame([input_dict])

        df_engineered = feature_engineering(df_input)

        # Ensure all required features exist and are ordered as expected by model
        df_final = pd.DataFrame(columns=features_list)
        for col in features_list:
            df_final[col] = df_engineered[col] if col in df_engineered.columns else 0

        df_final = df_final[features_list]

        prediction = models[request.mode].predict(df_final)[0]

        return PredictionResponse(predicted_price=round(float(prediction), 2))

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.exception_handler(Exception)
def validation_exception_handler(request, exc):
    logger.error(f"Validation Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": "Invalid input or server error."},
    )