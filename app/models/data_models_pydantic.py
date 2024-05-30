
from pydantic import BaseModel, Field

class SapInput(BaseModel):
    details: dict

class GmaoInput(BaseModel):
    details: dict

class ClearInput(BaseModel):
    details: dict

class BimInput(BaseModel):
    details: dict

class CombinedDataInput(BaseModel):
    sap: SapInput = Field(default_factory=SapInput)
    gmao: GmaoInput = Field(default_factory=GmaoInput)
    clear: ClearInput = Field(default_factory=ClearInput)
    bim: BimInput = Field(default_factory=BimInput)