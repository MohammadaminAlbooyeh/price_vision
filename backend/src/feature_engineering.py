import pandas as pd

def feature_engineering(data):
    """Perform feature extraction and transformation."""
    # Create new features for Italy House Prices
    # 'superficie' is Area (SF in US context)
    if 'superficie' in data.columns and 'stanze' in data.columns:
        data['Area_per_Room'] = data['superficie'] / (data['stanze'] + 1)
    
    # Combination of bathroom/room ratio already exists but let's add one if not
    if 'bagni' in data.columns and 'stanze' in data.columns:
        data['Bathroom_Ratio'] = data['bagni'] / (data['stanze'] + 1)

    # Boolean combinations
    if all(col in data.columns for col in ['balcone', 'giardino privato']):
        data['Has_Outdoor_Space'] = (data['balcone'] == 1) | (data['giardino privato'] == 1)
        data['Has_Outdoor_Space'] = data['Has_Outdoor_Space'].astype(int)

    return data

# Example usage
if __name__ == "__main__":
    data = pd.read_csv("../data/processed/train_processed.csv")
    engineered_data = feature_engineering(data)
    engineered_data.to_csv("../data/processed/train_engineered.csv", index=False)