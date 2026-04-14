"""
validators.py
Funciones para validar entradas del usuario y evitar errores en tiempo de ejecución.
"""
import re
from datetime import datetime

def validar_monto(monto_str: str):
    """Valida que el monto sea un número positivo."""
    try:
        monto = float(monto_str.replace(",", "."))
        if monto <= 0:
            return None, "El monto debe ser mayor a 0."
        return monto, None
    except ValueError:
        return None, "Formato numérico inválido. Usa punto o coma para decimales."

def validar_categoria(categoria: str, validas: list):
    """Valida que la categoría exista en la lista permitida."""
    categoria = categoria.lower().strip()
    if categoria in validas:
        return categoria, None
    return None, f"Categoría no válida. Opciones: {', '.join(validas)}"

def validar_fecha(fecha_str: str):
    """Valida formato YYYY-MM-DD y que no sea futura."""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha_str):
        return None, "Formato inválido. Usa YYYY-MM-DD."
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        if fecha.date() > datetime.now().date():
            return None, "La fecha no puede ser futura."
        return fecha_str, None
    except ValueError:
        return None, "Fecha no válida (ej: 30/02/2025 es inválido)."