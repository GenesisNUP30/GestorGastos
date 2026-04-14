"""
visualizer.py
Generación de gráficos interactivos con Matplotlib. Muestra el gráfico en pantalla inmediatamente.
"""
import matplotlib.pyplot as plt
from colorama import Fore, Style

def generar_grafico(resumen: dict):
    """
    Genera y MUESTRA EN PANTALLA un gráfico de barras con la distribución de gastos.
    La ventana se cierra al pulsar 'X' o al presionar Enter tras cerrarla.
    """
    if not resumen:
        print(f"{Fore.YELLOW}⚠️ No hay datos suficientes para generar el gráfico.{Style.RESET_ALL}")
        return
    
    categorias = list(resumen.keys())
    montos = [round(m, 2) for m in resumen.values()]  # Redondear para etiquetas limpias
    colores = plt.cm.Set3.colors[:len(categorias)]

    # Crear figura con tamaño adecuado para presentación
    plt.figure(figsize=(10, 6))
    barras = plt.bar(categorias, montos, color=colores, edgecolor="black", linewidth=1.2)
    
    # Títulos y etiquetas con estilo profesional
    plt.title("📊 Distribución de Gastos por Categoría", fontsize=16, fontweight="bold", pad=20)
    plt.xlabel("Categorías", fontsize=12, fontweight="semibold")
    plt.ylabel("Gasto (€)", fontsize=12, fontweight="semibold")
    plt.xticks(rotation=25, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.5, linewidth=0.5)
    
    # Añadir etiquetas de valor sobre cada barra
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
    
    # 🎯 MOSTRAR EN PANTALLA (bloqueante hasta cerrar la ventana)
    print(f"\n{Fore.CYAN}🔍 Se abrirá una ventana con el gráfico. Ciérrala para continuar...{Style.RESET_ALL}")
    plt.show()  # ← ESTO MUESTRA EL GRÁFICO EN PANTALLA
    
    print(f"{Fore.GREEN}✅ Gráfico cerrado. Volviendo al menú principal...{Style.RESET_ALL}")