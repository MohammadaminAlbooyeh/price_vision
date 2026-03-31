import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from data_preprocessing import preprocess_data
from feature_engineering import feature_engineering
from validation import validate_dataframe

def train_model():
    """Main training pipeline with hyperparameter tuning and model comparison."""
    sale_path = "backend/data/raw/sale_clean.csv"
    rent_path = "backend/data/raw/rents_clean.csv"

    if not os.path.exists(sale_path):
        sale_path = "data/raw/sale_clean.csv"
    if not os.path.exists(rent_path):
        rent_path = "data/raw/rents_clean.csv"

    if not os.path.exists(sale_path) and not os.path.exists(rent_path):
        raise FileNotFoundError("No training files found in backend/data/raw or data/raw")

    frames = []
    if os.path.exists(sale_path):
        sale_data = pd.read_csv(sale_path)
        sale_data['mode'] = 'sale'
        frames.append(sale_data)
    if os.path.exists(rent_path):
        rent_data = pd.read_csv(rent_path)
        rent_data['mode'] = 'rent'
        frames.append(rent_data)

    data = pd.concat(frames, ignore_index=True)
    print('Initial total rows', len(data))

    data = validate_dataframe(data)
    print('After validation', len(data))

    temp_path = 'backend/data/raw/combined_train_for_model.csv'
    data.to_csv(temp_path, index=False)

    data = preprocess_data(temp_path)

    if 'prezzo' not in data.columns:
        raise ValueError("Target column 'prezzo' not found.")

    print('Processed data shape', data.shape)

    data = feature_engineering(data)
    print('Engineered data shape', data.shape)

    # Train separate models for sale and rent
    for mode in ['sale', 'rent']:
        print(f"Training model for mode={mode}...")
        if f'mode_{mode}' not in data.columns:
            print(f"Skipping {mode}: no data for this mode after preprocessing")
            continue

        subset = data[data[f'mode_{mode}'] == 1].copy()
        if subset.empty:
            print(f"No data for mode={mode}")
            continue

        X = subset.drop(columns=['prezzo'])
        y = subset['prezzo']

        # Drop other mode columns from features to avoid collinearity
        mode_cols = [c for c in X.columns if c.startswith('mode_')]
        X = X.drop(columns=mode_cols)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf = RandomForestRegressor(random_state=42)
        param_grid = {
            'n_estimators': [50, 100],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        }

        grid_search = GridSearchCV(rf, param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1)
        grid_search.fit(X_train, y_train)
        best_rf = grid_search.best_estimator_

        lr = LinearRegression(); lr.fit(X_train, y_train)

        rf_preds = best_rf.predict(X_test)
        lr_preds = lr.predict(X_test)

        print(f"{mode} Random Forest MAE: {mean_absolute_error(y_test, rf_preds):.2f}, R2: {r2_score(y_test, rf_preds):.2f}")
        print(f"{mode} Linear Regression MAE: {mean_absolute_error(y_test, lr_preds):.2f}, R2: {r2_score(y_test, lr_preds):.2f}")

        model_dir = "backend/models" if os.path.exists("backend") else "models"
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump(best_rf, os.path.join(model_dir, f"model_{mode}.pkl"))

    joblib.dump(list(X.columns), os.path.join(model_dir, "features.pkl"))
    print("Models and feature list saved.")

if __name__ == "__main__":
    train_model()
