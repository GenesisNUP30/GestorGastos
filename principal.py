"""
principal.py
Punto de entrada del proyecto. Configura el presupuesto del mes actual y lanza el menú.
Manejo robusto de interrupciones y alineado con el sistema de presupuestos por mes.
"""
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# Añade la raíz del proyecto al sys.path para garantizar la resolución de imports relativos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG_FILE
from datos.almacenamiento import cargar_configuracion, guardar_configuracion
from interfaz.menu_consola import mostrar_menu, ejecutar_opcion, limpiar_pantalla


def main():
    limpiar_pantalla()
    print(f"{Fore.CYAN}Iniciando aplicación de Gestor de Gastos {Style.RESET_ALL}")
    
    # Formato interno para lógica y almacenamiento (YYYY-MM)
    mes_actual_iso = datetime.now().strftime("%Y-%m")
    # Formato visual para mensajes al usuario (MM/YYYY)
    mes_actual_visual = datetime.now().strftime("%m/%Y")

    # Carga configuración persistente y verifica si ya existe un presupuesto para este mes
    config = cargar_configuracion(CONFIG_FILE)
    presupuestos = config.get("presupuestos", {})
    presupuesto_actual = presupuestos.get(mes_actual_iso)

    if presupuesto_actual is None:
        print(f"{Fore.YELLOW}💡 Es la primera vez que registras gastos para {mes_actual_visual}.{Style.RESET_ALL}")
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
                presupuestos[mes_actual_iso] = presupuesto_actual
                config["presupuestos"] = presupuestos
                guardar_configuracion(CONFIG_FILE, config)
                print(f"{Fore.GREEN}✅ Presupuesto de {presupuesto_actual:.2f}€ guardado para {mes_actual_visual}.{Style.RESET_ALL}")
                break
            except ValueError:
                print(f"{Fore.RED}❌ Introduce un número válido mayor a 0.{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}📌 Presupuesto cargado para {mes_actual_visual}: {presupuesto_actual:.2f}€{Style.RESET_ALL}")

    # Bucle principal de la aplicación con manejo seguro de interrupciones
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