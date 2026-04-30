"""
visualizador.py
Capa de visualización de datos. Utiliza Matplotlib para generar gráficos de barras
interactivos que muestran la distribución de gastos por categoría, abriéndose en
una ventana nativa del sistema para análisis detallado.
"""
import matplotlib.pyplot as plt
from colorama import Fore, Style

def generar_grafico(resumen: dict):
    """
    Genera y muestra en pantalla un gráfico de barras con la distribución de gastos.
    Bloquea la ejecución hasta que el usuario cierra la ventana.
    """
    if not resumen:
        print(f"{Fore.YELLOW}⚠️ No hay datos suficientes para generar el gráfico.{Style.RESET_ALL}")
        return
    
    # Preparación de datos: extrae categorías, redondea montos y asigna colores distintivos
    categorias = list(resumen.keys())
    montos = [round(m, 2) for m in resumen.values()]  # Redondear para etiquetas limpias
    colores = plt.cm.Set3.colors[:len(categorias)]

    # Configuración de la figura: tamaño y estilo base
    plt.figure(figsize=(10, 6))
    barras = plt.bar(categorias, montos, color=colores, edgecolor="black", linewidth=1.2)
    
    # Personalización de ejes, títulos y rejilla para legibilidad profesional
    plt.title("📊 Distribución de Gastos por Categoría", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Categorías", fontsize=12, fontweight="semibold")
    plt.ylabel("Gasto (€)", fontsize=12, fontweight="semibold")
    plt.xticks(rotation=25, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5, linewidth=0.5)
    
    # Etiquetas de valor sobre cada barra para lectura directa de montos
    for b in barras:
        height = b.get_height()
        plt.annotate(f'{height:.2f}€', 
                     xy=(b.get_x() + b.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom', 
                     fontsize=9, fontweight="bold",
                     bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.3))

    # Ajustar layout para que no se corten las etiquetas
    plt.tight_layout()
    
    # Mostrar gráfico en ventana interactiva (ejecución bloqueante hasta cierre)
    print(f"\n{Fore.CYAN}🔍 Se abrirá una ventana con el gráfico. Ciérrala para continuar...{Style.RESET_ALL}")
    plt.show()
    
    print(f"{Fore.GREEN}✅ Gráfico cerrado. Volviendo al menú principal...{Style.RESET_ALL}")