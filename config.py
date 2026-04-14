"""
config.py
Configuración global del proyecto. Define rutas, categorías por defecto y parámetros visuales.
"""
import os

# Rutas de almacenamiento y reportes (se crean automáticamente si no existen)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "almacen_datos")
REPORTES_DIR = os.path.join(BASE_DIR, "informes")
EXPENSES_FILE = os.path.join(DATA_DIR, "gastos.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

# Categorías predefinidas
DEFAULT_CATEGORIES = ["comida", "transporte", "ocio", "estudio", "salud", "otros"]

# Configuración visual
CHART_FILENAME = "grafico_gastos.png"
EXPORT_FILENAME = "resumen_gastos.txt"