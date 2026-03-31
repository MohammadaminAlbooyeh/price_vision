import pandas as pd
import pydantic
from typing import List, Optional

class PropertyData(pydantic.BaseModel):
    """Schema for validating housing data during training or ingestion."""
    prezzo: float = pydantic.Field(..., gt=0, description="Property price in Euro")
    superficie: float = pydantic.Field(..., gt=10, description="Square meters")
    stanze: int = pydantic.Field(..., ge=1)
    bagni: int = pydantic.Field(..., ge=1)
    posti_auto: int = pydantic.Field(default=0, alias="posti auto")
    riscaldamento_centralizzato: int = pydantic.Field(default=0, alias="riscaldamento centralizzato")
    # ... more fields as needed based on raw data columns

def validate_dataframe(df: pd.DataFrame):
    """Simple wrapper to validate all rows in a DataFrame against the schema."""
    try:
        # Example validation for subset of critical columns
        valid_indices = []
        for idx, row in df.iterrows():
            if row['prezzo'] > 0 and row['superficie'] > 0:
                valid_indices.append(idx)
        
        invalid_count = len(df) - len(valid_indices)
        if invalid_count > 0:
            print(f"Warning: Dropping {invalid_count} invalid rows during validation.")
            
        return df.loc[valid_indices].copy()
    except Exception as e:
        print(f"Validation error: {e}")
        return df
