"""
validadores.py
Funciones para validar entradas del usuario y evitar errores en tiempo de ejecución.
"""
import re
from datetime import datetime

def validar_monto(monto_str: str):
    """Valida que la entrada de la cantidad del gasto sea un número positivo."""
    try:
        monto = float(monto_str.replace(",", "."))
        if monto <= 0:
            return None, "El monto debe ser mayor a 0."
        return monto, None
    except ValueError:
        return None, "Formato numérico inválido. Usa punto o coma para decimales."

def validar_categoria(categoria: str, validas: list):
    """Valida que la categoría exista en la lista de opciones permitida."""
    categoria = categoria.lower().strip()
    if categoria in validas:
        return categoria, None
    return None, f"Categoría no válida. Opciones: {', '.join(validas)}"

def validar_fecha(fecha_str: str):
    """Valida formato DD-MM-YYYY (o DD/MM/YYYY) y que no sea futura. Devuelve YYYY-MM-DD para almacenamiento."""
    if not fecha_str:
        return None, "La fecha no puede estar vacía."

    # Normaliza separadores para aceptar tanto barras como guiones
    fecha_str = fecha_str.replace("/", "-")

    try:
        fecha_obj = datetime.strptime(fecha_str, "%d-%m-%Y")
    except ValueError:
        return None, "Formato inválido. Usa DD-MM-YYYY (ej: 15-04-2024)."

    if fecha_obj.date() > datetime.now().date():
        return None, "La fecha no puede ser futura."

    # Convierte al formato interno YYYY-MM-DD para que los filtros por mes funcionen correctamente
    return fecha_obj.strftime("%Y-%m-%d"), None