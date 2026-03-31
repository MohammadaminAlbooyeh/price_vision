from pydantic import BaseModel, Field
from typing import Optional

class PredictionRequest(BaseModel):
    mode: str = Field("sale", description="Property type: sale or rent")
    superficie: float = Field(..., description="Surface area in square meters", gt=0)
    stanze: int = Field(..., description="Number of rooms", ge=0)
    bagni: int = Field(..., description="Number of bathrooms", ge=0)
    # The aliases below must match exactly the column names in training/CSV
    posti_auto: int = Field(0, alias="posti auto")
    ultimo_piano: int = Field(0, alias="ultimo piano")
    vista_mare: int = Field(0, alias="vista mare")
    riscaldamento_centralizzato: int = Field(0, alias="riscaldamento centralizzato")

    arredato: int = Field(0)
    balcone: int = Field(0)
    impianto_tv: int = Field(0, alias="impianto tv")
    esposizione_esterna: int = Field(0, alias="esposizione externa")
    fibra_ottica: int = Field(0, alias="fibra ottica")
    cancello_elettrico: int = Field(0, alias="cancello elettrico")
    cantina: int = Field(0)
    giardino_comune: int = Field(0, alias="giardino comune")
    giardino_privato: int = Field(0, alias="giardino privato")
    impianto_allarme: int = Field(0, alias="impianto allarme")
    portiere: int = Field(0)
    piscina: int = Field(0)
    villa: int = Field(0)
    intera_proprieta: int = Field(0, alias="intera proprieta")
    appartamento: int = Field(1)
    attico: int = Field(0)
    loft: int = Field(0)
    mansarda: int = Field(0)
    year: int = Field(2026)
    month: int = Field(3)

    class Config:
        populate_by_name = True

class PredictionResponse(BaseModel):
    predicted_price: float