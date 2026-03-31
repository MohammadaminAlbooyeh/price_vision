import pandas as pd

def preprocess_data(file_path):
    """Preprocess raw data for training."""
    # Load the data
    data = pd.read_csv(file_path)

    # Convert datetime to numeric if needed (for simplicity, we'll extract the year)
    if 'datetime' in data.columns:
        data['datetime'] = pd.to_datetime(data['datetime'])
        data['year'] = data['datetime'].dt.year
        data['month'] = data['datetime'].dt.month
        data.drop(columns=['datetime'], inplace=True)

    # Drop columns with too many missing values or irrelevant strings
    # 'regione' and 'citta' might be useful but need encoding.
    # For a quick CV-ready baseline, we'll keep numeric features and handle missing.

    # Handle missing values
    numeric_cols = data.select_dtypes(include=['number']).columns
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].median())

    # Encode categorical variables (limited to columns with low cardinality for now)
    categorical_cols = ['regione', 'stato', 'classe energetica', 'mode']
    for col in categorical_cols:
        if col in data.columns:
            # Mode column should preserve both sale/rent flags, so do not drop first when mode
            drop_first = False if col == 'mode' else True
            data = pd.get_dummies(data, columns=[col], drop_first=drop_first)

    # Drop non-numeric columns that weren't encoded (like citta, quartiere if too many)
    # Include boolean dummy columns because get_dummies may produce booleans.
    data = data.select_dtypes(include=['number', 'bool'])
    # Convert bool columns to int so ML models handle them consistently
    bool_cols = data.select_dtypes(include=['bool']).columns
    data[bool_cols] = data[bool_cols].astype(int)

    return data

# Example usage
if __name__ == "__main__":
    processed_data = preprocess_data("../data/raw/train.csv")
    processed_data.to_csv("../data/processed/train_processed.csv", index=False)