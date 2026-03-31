from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to PriceVision API"}

def test_predict_invalid_data():
    response = client.post("/predict", json={"invalid": "data"})
    assert response.status_code == 400
