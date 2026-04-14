"""
main.py
Punto de entrada del proyecto. Inicializa configuración y lanza el menú interactivo.
"""
import sys
import os
from colorama import init, Fore, Style
init(autoreset=True)

# Asegura que los paquetes internos se resuelvan correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.console_menu import mostrar_menu, ejecutar_opcion, limpiar_pantalla

def main():
    limpiar_pantalla()
    print(f"{Fore.CYAN}🚀 Iniciando Gestor de Gastos Estudiantil v1.0...{Fore.RESET}")
    
    try:
        pres_str = input(f"{Fore.YELLOW}💡 Presupuesto mensual (€) o Enter para ilimitado: {Fore.RESET}").strip()
        presupuesto = float(pres_str) if pres_str else None
        if presupuesto is not None and presupuesto <= 0:
            print(f"{Fore.RED}⚠️ Presupuesto inválido. Se desactivará el control mensual.{Fore.RESET}")
            presupuesto = None
    except ValueError:
        print(f"{Fore.RED}⚠️ Entrada no numérica. Presupuesto desactivado.{Fore.RESET}")
        presupuesto = None

    while True:
        mostrar_menu()
        opcion = input(f"{Fore.WHITE}👉 Selecciona opción: {Fore.RESET}").strip()
        try:
            ejecutar_opcion(opcion, presupuesto)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️ Interrupción manual. Saliendo...{Fore.RESET}")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}❌ Error crítico: {e}. Revisa la consola o contacta soporte.{Fore.RESET}")

if __name__ == "__main__":
    main()