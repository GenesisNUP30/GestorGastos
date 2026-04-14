"""
formatters.py
Utilidades para formatear monedas, fechas y textos de salida.
"""
def formato_moneda(valor: float) -> str:
    """Formatea números como moneda europea."""
    return f"{valor:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")

def formato_fecha(fecha_str: str) -> str:
    """Convierte YYYY-MM-DD a DD/MM/YYYY."""
    from datetime import datetime
    dt = datetime.strptime(fecha_str, "%Y-%m-%d")
    return dt.strftime("%d/%m/%Y")