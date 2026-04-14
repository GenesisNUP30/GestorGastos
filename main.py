"""
main.py
Punto de entrada del proyecto. Inicializa configuración y lanza el menú interactivo.
Manejo robusto de interrupciones y alineado con el sistema de presupuestos por mes.
"""
import sys
import os
from colorama import init, Fore, Style
init(autoreset=True)

# Asegura que los paquetes internos se resuelven correctamente desde la raíz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.console_menu import mostrar_menu, ejecutar_opcion, limpiar_pantalla

def main():
    limpiar_pantalla()
    print(f"{Fore.CYAN}🚀 Iniciando Gestor de Gastos Estudiantil {Fore.RESET}")

    try:
        while True:
            mostrar_menu()
            # El try/except ahora cubre el input para capturar Ctrl+C en cualquier momento
            opcion = input(f"{Fore.WHITE}👉 Selecciona opción: {Fore.RESET}").strip()
            ejecutar_opcion(opcion)
            
    except KeyboardInterrupt:
        # Salida elegante cuando el usuario pulsa Ctrl+C
        print(f"\n\n{Fore.YELLOW}⚠️ Interrupción detectada. Saliendo del programa...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}👋 ¡Hasta la próxima!{Fore.RESET}")
        sys.exit(0)
    except Exception as e:
        # Captura cualquier error inesperado para evitar crashes feos
        print(f"\n{Fore.RED}❌ Error crítico inesperado: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Presiona Enter para salir...{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()