"""
formateadores.py
Utilidades para formatear monedas, fechas y textos de salida.
"""
from datetime import datetime

def formato_moneda(valor: float) -> str:
    """Convierte número a moneda con separadores de miles y decimales."""
    return f"{valor:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def formato_fecha_display(fecha_iso: str) -> str:
    """Convierte YYYY-MM-DD (interno) a DD-MM-YYYY (visual)."""
    try:
        fecha_obj = datetime.strptime(fecha_iso, "%Y-%m-%d")
        return fecha_obj.strftime("%d-%m-%Y")
    except ValueError:
        return fecha_iso