"""
main.py
Punto de entrada del proyecto. Configura el presupuesto del mes actual y lanza el menú.
Manejo robusto de interrupciones y alineado con el sistema de presupuestos por mes.
"""
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# Asegura que los paquetes internos se resuelven correctamente desde la raíz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG_FILE
from data.storage import cargar_configuracion, guardar_configuracion
from ui.console_menu import mostrar_menu, ejecutar_opcion, limpiar_pantalla


def main():
    limpiar_pantalla()
    print(f"{Fore.CYAN}🚀 Iniciando Gestor de Gastos Estudiantil v2.2...{Style.RESET_ALL}")

    # Configuración inicial del presupuesto para el mes actual
    mes_actual = datetime.now().strftime("%Y-%m")
    config = cargar_configuracion(CONFIG_FILE)
    presupuestos = config.get("presupuestos", {})
    presupuesto_actual = presupuestos.get(mes_actual)

    if presupuesto_actual is None:
        print(f"{Fore.YELLOW}💡 Es la primera vez que usas {mes_actual}.{Style.RESET_ALL}")
        while True:
            entrada = input(
                f"{Fore.WHITE}💰 Introduce presupuesto para este mes (€) o [Enter] para ilimitado: {Style.RESET_ALL}"
            ).strip()
            if not entrada:
                presupuesto_actual = None
                print(f"{Fore.CYAN}📊 Modo presupuesto desactivado.{Style.RESET_ALL}")
                break
            try:
                presupuesto_actual = float(entrada.replace(",", "."))
                if presupuesto_actual <= 0:
                    raise ValueError
                presupuestos[mes_actual] = presupuesto_actual
                config["presupuestos"] = presupuestos
                guardar_configuracion(CONFIG_FILE, config)
                print(f"{Fore.GREEN}✅ Presupuesto de {presupuesto_actual:.2f}€ guardado para {mes_actual}.{Style.RESET_ALL}")
                break
            except ValueError:
                print(f"{Fore.RED}❌ Introduce un número válido mayor a 0.{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}📌 Presupuesto cargado para {mes_actual}: {presupuesto_actual:.2f}€{Style.RESET_ALL}")

    print(f"{Fore.YELLOW}💡 Tip: Usa las opciones 5, 6 o 7 para ver resúmenes y gráficos por mes.{Fore.RESET}\n")

    try:
        while True:
            mostrar_menu()
            opcion = input(f"{Fore.WHITE}👉 Selecciona opción: {Fore.RESET}").strip()
            ejecutar_opcion(opcion)
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}⚠️ Interrupción detectada. Saliendo del programa...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}👋 ¡Hasta la próxima!{Fore.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error crítico inesperado: {e}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Presiona Enter para salir...{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()