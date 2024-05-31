"""
Router para la gestión de datos del producto de dashboard.
"""

from fastapi import APIRouter, HTTPException

from app.data_products.product_dashboard.data_contract_service import (
    validate_data_with_datacontract,
    send_data_to_api
)
from app.data_products.product_dashboard.transformers import (
    transform_sap_data,
    transform_gmao_data,
    transform_clear_data,
    transform_bim_data,
    combine_data
)
from app.models.data_models_pydantic import CombinedDataInput

router = APIRouter()

@router.post("/process_data/")
async def process_data(data: CombinedDataInput):
    """
    Recibe los datos, los manda a transformar (transformers), los manda a combinarlos para generar el Json (transformers),
    manda el Json a validar con datacontract - cli (data_contract_service ) y
    si se valida correctamente los envía a nuestra API.
    """
    try:
        # Asigna los datos a cada función de transformación según corresponda
        transformed_data_sap = transform_sap_data(data.sap)
        transformed_data_gmao = transform_gmao_data(data.gmao)
        transformed_data_clear = transform_clear_data(data.clear)
        transformed_data_bim = transform_bim_data(data.bim)

        # Combina todos los datos transformados en una estructura única
        combined_data = combine_data(
            transformed_data_sap,
            transformed_data_gmao,
            transformed_data_clear,
            transformed_data_bim
        )

        # Validar los datos antes de enviarlos, los mandamos a validar
        if validate_data_with_datacontract(combined_data):
            # Si la validación ha sido correcta se envía el JSON
            response = send_data_to_api(
                combined_data,
                "endpoint para dashboard en la API de vt-lab"
            )
            return {"message": "Data sent successfully", "api_response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
