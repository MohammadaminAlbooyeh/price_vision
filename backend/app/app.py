from fastapi import FastAPI
import joblib
import pandas as pd
from typing import List

app = FastAPI(title="PriceVision API")

# Load model (placeholder for when model.pkl is ready)
# model = joblib.load("../models/model.pkl")

@app.get("/")
def read_root():
    return {"message": "Welcome to PriceVision API"}

@app.post("/predict")
def predict(data: dict):
    # logic for prediction using model.pkl
    return {"prediction": "TBD"}
