"""
Este módulo contiene funciones para transformar datos de diferentes fuentes al formato esperado.
"""

from datetime import datetime


def transform_sap_data(data: dict) -> dict:
    """
    Transforma los datos de SAP al formato esperado.
    """
    return {
        "Planta": data.get("sap_plant", ""),
        "Gasto_trabajadores": float(data.get("employee_costs", "").replace("€", ""))
    }

def transform_gmao_data(data: dict) -> dict:
    """
    Transforma los datos de GMAO al formato esperado.
    """
    return {
        "Planta": data.get("gmao_location", ""),
        "Lineas_de_trabajo": [
            {
                "ID_Linea": line.get("workline_id", ""),
                "nombre_linea_de_trabajo": line.get("workline_title", ""),
                "entrada_material": 0,
                "producto_Salida": [],
                "consumo_electrico": float(line.get("electric_usage", "").split()[0]),
                "tiempo_de_paro": float(line.get("downtime_total", ""))
            }
            for line in data.get("gmao_worklines", [])
        ]
    }

def transform_clear_data(data: dict) -> dict:
    """
    Transforma los datos de CLEAR al formato esperado.
    """
    return {
        "Planta": "",
        "Lineas_de_trabajo": [
            {
                "ID_Linea": data.get("line_id", ""),  # Asumimos que CLEAR también proporciona ID
                "nombre_linea_de_trabajo": "",  # Nombre desde BIM
                "entrada_material": float(data.get("input_material", "").split()[0]),
                "producto_Salida": [
                    {
                        "tipo_material": product.get("product_type", ""),
                        "cantidad": float(product.get("product_amount", ""))
                    }
                    for product in data.get("output_products", [])
                ],
                "consumo_electrico": 0,  # Desde GMAO
                "tiempo_de_paro": 0  # Desde GMAO
            }
        ],
        "Gasto_trabajadores": 0  # Desde SAP
    }

def transform_bim_data(data: dict) -> dict:
    """
    Transforma los datos de BIM al formato esperado.
    """
    return {
        "Planta": data.get("plant_location", ""),
        "Lineas_de_trabajo": [
            {
                "ID_Linea": line["ID_Linea"],  # Identificador de línea proporcionado por BIM
                "nombre_linea_de_trabajo": line["line_name"],  # Asumimos que BIM proporciona el nombre
                "entrada_material": 0,  # Desde CLEAR
                "producto_Salida": [],  # Desde CLEAR
                "consumo_electrico": 0,  # Desde GMAO
                "tiempo_de_paro": 0  # Desde GMAO
            }
            for line in data.get("bim_worklines", [])
        ],
        "Gasto_trabajadores": 0  # Desde SAP
    }

def combine_data(sap_data, gmao_data, clear_data, bim_data):
    """
    Combina los datos transformados de SAP, GMAO, CLEAR y BIM en un único diccionario.
    """

    # Obtener el timestamp actual en el formato deseado
    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    combined = {
        "metadata": {
            "timestamp": current_timestamp,
            "version": "1.0",
            "units": {
                "consumo_electrico": "kW",
                "tiempo_paro": "minutos",
                "gasto_trabajadores": "€",
                "cantidad": "Toneladas",
                "periocidad_de_los_datos": ["dia", "semana", "mes", "año"]
            }
        },
        "Planta": bim_data["Planta"],
        "Lineas_de_trabajo": [],
        "Gasto_trabajadores": sap_data["Gasto_trabajadores"]
    }

    # Fusiona las líneas de trabajo con datos de todas las fuentes
    for bim_line in bim_data["Lineas_de_trabajo"]:
        line_id = bim_line["ID_Linea"]
        gmao_line = next((line for line in gmao_data["Lineas_de_trabajo"] if line["ID_Linea"] == line_id), None)
        clear_line = next((line for line in clear_data["Lineas_de_trabajo"] if line["ID_Linea"] == line_id), None)

        # Combinar información de todas las fuentes
        combined_line = {
            "ID_Linea": line_id,
            "nombre_linea_de_trabajo": bim_line["nombre_linea_de_trabajo"],
            "consumo_electrico": gmao_line["consumo_electrico"] if gmao_line else 0,
            "tiempo_de_paro": gmao_line["tiempo_de_paro"] if gmao_line else 0,
            "entrada_material": clear_line["entrada_material"] if clear_line else 0,
            "producto_Salida": clear_line["producto_Salida"] if clear_line else []
        }

        combined["Lineas_de_trabajo"].append(combined_line)

    return combined
