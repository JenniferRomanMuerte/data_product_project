"""
Este módulo contiene funciones para transformar y enviar datos a otra API.
"""

import requests
from fastapi import HTTPException

import subprocess
import yaml
import json


def validate_data_with_datacontract(combined_data, data_contract_path="app/data_contracts/datacontract.yaml"):
    """
    Valida los datos combinados usando datacontract-cli.
    """
    # Guardar los datos en un archivo JSON temporal
    timestamp = combined_data["metadata"]["timestamp"].replace(':', '').replace('-', '').replace('T', '_').replace('Z', '')
    filename = f"app/uploads/{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(combined_data, file, ensure_ascii=False, indent=2)
    
    # Actualizar el archivo de contrato de datos para referenciar el archivo subido
    with open(data_contract_path, "r", encoding="utf-8") as yaml_file:
        datacontract = yaml.safe_load(yaml_file)
    datacontract['servers']['production']['path'] = filename
    with open(data_contract_path, "w", encoding="utf-8") as yaml_file:
        yaml.safe_dump(datacontract, yaml_file)

    # Ejecutar la validación con datacontract-cli
    result = subprocess.run(['datacontract', 'test', data_contract_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Validation failed: {result.stderr}")

    return True  # Retorna True si la validación fue exitosa


def send_data_to_api(transformed_data: dict, target_url: str):
    """
    Envía los datos ya transformados a otra API.

    Args:
        transformed_data (dict): Los datos ya transformados.
        target_url (str): La URL de la API de destino.

    Returns:
        dict: La respuesta de la API de destino.

    Raises:
        HTTPException: Si la respuesta de la API no es satisfactoria.
    """
    response = requests.post(target_url, json=transformed_data, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

