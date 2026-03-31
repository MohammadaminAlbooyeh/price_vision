# PriceVision: Italy House Price Prediction

A professional full-stack machine learning application for predicting residential property prices in Italy. This project leverages real-world Italian real estate data to provide accurate valuations based on property characteristics and regional trends.

## Features
- **Modern UI**: React-based dashboard with real-time price trend visualization using Chart.js.
- **FastAPI Backend**: High-performance REST API with automated documentation.
- **Advanced ML Pipeline**: Automated preprocessing, feature engineering (Area-per-Room, Bathroom Ratios), and multi-model training (Random Forest vs. Linear Regression).
- **Pro Logging**: Comprehensive backend logging for auditing and debugging.

## Backend Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Backend
1. Start the FastAPI server:
   ```bash
   export PYTHONPATH=$PYTHONPATH:. && python3 -m uvicorn app.main:app --reload
   ```
2. Access the API documentation at:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Training the Model
1. Ensure the Italy dataset (`sale_clean.csv`) is in `data/raw/`.
2. Run the training script:
   ```bash
   python3 train.py
   ```
3. The trained model will be saved in `models/model.pkl`.

## Frontend Setup

### Prerequisites
- Node.js 18+
- npm

### Installation
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Frontend
1. Start the Vite development server:
   ```bash
   npm run dev
   ```
2. View the application at:
   [http://localhost:5173](http://localhost:5173)