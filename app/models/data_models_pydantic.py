"""
Módulo que define las clases de entrada para diferentes sistemas y sus combinaciones.
"""

from pydantic import BaseModel, Field

class SapInput(BaseModel):
    """
    Clase que representa los datos de entrada para el sistema SAP.

    Atributos:
    details: Diccionario con los detalles específicos del sistema SAP.
    """
    details: dict

class GmaoInput(BaseModel):
    """
    Clase que representa los datos de entrada para el sistema GMAO.

    Atributos:
    details: Diccionario con los detalles específicos del sistema GMAO.
    """
    details: dict

class ClearInput(BaseModel):
    """
    Clase que representa los datos de entrada para el sistema CLEAR.

    Atributos:
    details: Diccionario con los detalles específicos del sistema CLEAR.
    """
    details: dict

class BimInput(BaseModel):
    """
    Clase que representa los datos de entrada para el sistema BIM.

    Atributos:
    details: Diccionario con los detalles específicos del sistema BIM.
    """
    details: dict

class CombinedDataInput(BaseModel):
    """
    Clase que combina los datos de entrada de varios sistemas en una sola estructura.

    Atributos:
    sap: Datos de entrada para el sistema SAP.
    gmao: Datos de entrada para el sistema GMAO.
    clear: Datos de entrada para el sistema CLEAR.
    bim: Datos de entrada para el sistema BIM.
    """
    sap: SapInput = Field(default_factory=SapInput)
    gmao: GmaoInput = Field(default_factory=GmaoInput)
    clear: ClearInput = Field(default_factory=ClearInput)
    bim: BimInput = Field(default_factory=BimInput)

# Fin del archivo
