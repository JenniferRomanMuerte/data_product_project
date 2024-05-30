"""
Este módulo contiene pruebas para los transformadores de datos.
"""
import yaml
import json
import subprocess

from app.service.transformers import (
    transform_sap_data,
    transform_gmao_data,
    transform_clear_data,
    transform_bim_data,
    combine_data
)


def test_combined_data():
    """
    Prueba la combinación de datos transformados de SAP, GMAO, CLEAR y BIM.
    """
    sap_data = {

        "employee_costs": "25000€",
        "sap_plant": "Zona Franca"
    }

    gmao_data = {
        "gmao_location": "Zona Franca",
        "gmao_worklines": [
            {
                "workline_id": "L1",
                "workline_title": "Tratamiento industriales y otros",
                "electric_usage": "1200 kW",
                "downtime_total": "90"
            }
        ]
    }

    clear_data = {
        "line_id": "L1",
        "input_material": "50 Toneladas",
        "output_products": [
            {
                "product_type": "Material A",
                "product_amount": "30"
            },
            {
                "product_type": "Material B",
                "product_amount": "20"
            }
        ]
    }

    bim_data = {
        "plant_location": "Zona Franca",
        "bim_worklines": [
            {
                "ID_Linea": "L1",
                "line_name": "Tratamiento industriales y otros"
            }
        ]
    }


    # Transformar los datos
    sap_transformed = transform_sap_data(sap_data)
    gmao_transformed = transform_gmao_data(gmao_data)
    clear_transformed = transform_clear_data(clear_data)
    bim_transformed = transform_bim_data(bim_data)

    # Combina los datos
    combined_json = combine_data(sap_transformed, gmao_transformed, clear_transformed, bim_transformed)

    # Convertir el timestamp para que sea adecuado como nombre de archivo
    timestamp = combined_json["metadata"]["timestamp"].replace(':', '').replace('-', '').replace('T', '_').replace('Z', '')
    filename = f"app/uploads/{timestamp}.json"

    print(json.dumps(combined_json, indent=2))

    # Guardar el resultado en un archivo nombrado con el timestamp
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(combined_json, file, ensure_ascii=False, indent=2)


    # Actualizar el archivo de contrato de datos para referenciar el archivo subido
    with open("app/data_contracts/datacontract.yaml", "r", encoding="utf-8") as yaml_file:
        datacontract = yaml.safe_load(yaml_file)
    datacontract['servers']['production']['path'] = filename
    with open("app/data_contracts/datacontract.yaml", "w", encoding="utf-8") as yaml_file:
        yaml.safe_dump(datacontract, yaml_file)

    # Ejecutar la validación
    result = subprocess.run(['datacontract', 'test', 'app/data_contracts/datacontract.yaml'], capture_output=True, text=True)
    print("Validation result:", result.stdout)

if __name__ == "__main__":
    test_combined_data()
