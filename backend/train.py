import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
from src.data_preprocessing import preprocess_data
from src.feature_engineering import feature_engineering

def train_models():
    """Train multiple models and save the best one or all of them."""
    # Preprocess the data (using the sale_clean dataset which contains price)
    data = preprocess_data("data/raw/sale_clean.csv")
    
    # Perform feature engineering
    data = feature_engineering(data)

    # Use 'prezzo' as Target (Price) instead of House Prices dataset's SalePrice
    if 'prezzo' not in data.columns:
        # Fallback for old training column naming mismatch
        raise ValueError("Column 'prezzo' not found in processed data.")
    
    X = data.drop(columns=['prezzo'], errors='ignore')
    X = X.select_dtypes(include=['number'])
    
    # Clean X
    X = X.fillna(X.mean())
    X = X.fillna(0)
    
    y = data['prezzo']

    # Handle cases where Price (y) contains 0 or NaN
    valid_indices = ~(y.isna() | (y == 0))
    X = X[valid_indices]
    y = y[valid_indices]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 1. Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_score = lr_model.score(X_test, y_test)
    print(f"Linear Regression R^2 Score: {lr_score}")

    # 2. Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_score = rf_model.score(X_test, y_test)
    print(f"Random Forest R^2 Score: {rf_score}")

    # Ensure models directory exists
    os.makedirs("models", exist_ok=True)

    # Save models
    joblib.dump(lr_model, "models/lr_model.pkl")
    joblib.dump(rf_model, "models/rf_model.pkl")
    
    # Export the feature names used for verification in loading
    joblib.dump(list(X.columns), "models/features.pkl")
    
    # Save best model as model.pkl
    best_model = lr_model if lr_score > rf_score else rf_model
    joblib.dump(best_model, "models/model.pkl")
    print(f"Saved best model: {'LinearRegression' if lr_score > rf_score else 'RandomForest'}")

if __name__ == "__main__":
    train_models()