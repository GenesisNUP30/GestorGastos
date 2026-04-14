"""
visualizer.py
Generación de gráficos profesionales con Matplotlib. Guarda automáticamente en reportes/.
"""
import os
import matplotlib.pyplot as plt
from config import REPORTS_DIR, CHART_FILENAME

def generar_grafico(resumen: dict):
    if not resumen:
        print("⚠️ No hay datos suficientes para generar el gráfico.")
        return
    
    categorias = list(resumen.keys())
    montos = list(resumen.values())
    colores = plt.cm.Set3.colors[:len(categorias)]

    plt.figure(figsize=(9, 5))
    barras = plt.bar(categorias, montos, color=colores, edgecolor="black")
    
    plt.title("Distribución de Gastos por Categoría", fontsize=14, fontweight="bold")
    plt.xlabel("Categorías", fontsize=12)
    plt.ylabel("Gasto (€)", fontsize=12)
    plt.xticks(rotation=30, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.6)

    # Etiquetas de valor sobre cada barra
    for b in barras:
        plt.annotate(f"{b.get_height():.2f}€", 
                     xy=(b.get_x() + b.get_width()/2, b.get_height()),
                     ha="center", va="bottom", fontweight="bold")

    ruta_final = os.path.join(REPORTS_DIR, CHART_FILENAME)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    plt.savefig(ruta_final, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"📈 Gráfico generado y guardado en: {ruta_final}")