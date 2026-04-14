"""
console_menu.py
Interfaz principal. Maneja el flujo de usuario, validaciones y llamadas a la lógica.
"""
import sys
from colorama import init, Fore, Style
init(autoreset=True)

from config import EXPENSES_FILE, DEFAULT_CATEGORIES, REPORTS_DIR, EXPORT_FILENAME
from data.storage import cargar_gastos, exportar_txt
from utils.validators import validar_monto, validar_categoria, validar_fecha
from core.expense_manager import agregar_gasto, resumen_por_categoria, filtrar_por_periodo, generar_reporte
from ui.visualizer import generar_grafico

def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print(f"\n{Fore.CYAN}{'='*45}")
    print(f"{Fore.YELLOW}💶 GESTOR DE GASTOS ESTUDIANTIL 💶")
    print(f"{Fore.CYAN}{'='*45}")
    print(f"{Fore.WHITE}1. ➕ Registrar nuevo gasto")
    print(f"{Fore.WHITE}2. 📊 Ver resumen + Gráfico visual")
    print(f"{Fore.WHITE}3. 💾 Exportar resumen a TXT")
    print(f"{Fore.WHITE}4. 📅 Filtrar por periodo")
    print(f"{Fore.WHITE}5. 🚪 Salir")
    print(f"{Fore.CYAN}{'='*45}")

def ejecutar_opcion(opcion: str, presupuesto_mensual: float = None):
    if opcion == "1":
        while True:
            monto, err = validar_monto(input("💰 Monto (ej: 15.50): ").strip())
            if err: print(f"{Fore.RED}❌ {err}")
            else: break
            
        while True:
            cat, err = validar_categoria(input(f"📂 Categoría ({', '.join(DEFAULT_CATEGORIES)}): ").strip(), DEFAULT_CATEGORIES)
            if err: print(f"{Fore.RED}❌ {err}")
            else: break
            
        desc = input("📝 Descripción (Enter=ninguna): ").strip() or "Sin descripción"
        
        while True:
            fecha_input = input("📅 Fecha (YYYY-MM-DD, Enter=hoy): ").strip()
            if not fecha_input:
                from datetime import datetime
                fecha_input = datetime.now().strftime("%Y-%m-%d")
            fecha, err = validar_fecha(fecha_input)
            if err: print(f"{Fore.RED}❌ {err}")
            else: break
            
        ok, msg = agregar_gasto(EXPENSES_FILE, monto, cat, desc, fecha)
        print(f"{Fore.GREEN if ok else Fore.RED}{msg}")

    elif opcion == "2":
        gastos = cargar_gastos(EXPENSES_FILE)
        periodo = input("📅 Periodo: semanal (s) / mensual (m) [m]: ").strip().lower() or "m"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        resumen = resumen_por_categoria(gastos_f)
        total = sum(resumen.values())
        limpiar_pantalla()
        print(generar_reporte(resumen, total, presupuesto_mensual))
        generar_grafico(resumen)
        input(f"{Fore.YELLOW}\nPresiona Enter para continuar...")

    elif opcion == "3":
        gastos = cargar_gastos(EXPENSES_FILE)
        periodo = input("📅 Exportar: semanal (s) / mensual (m) [m]: ").strip().lower() or "m"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        resumen = resumen_por_categoria(gastos_f)
        total = sum(resumen.values())
        txt = generar_reporte(resumen, total, presupuesto_mensual)
        ruta = f"{REPORTS_DIR}/gastos_{periodo if periodo=='s' else 'mensual'}.txt"
        if exportar_txt(ruta, txt):
            print(f"{Fore.GREEN}✅ Exportado a: {ruta}")
        input(f"{Fore.YELLOW}\nPresiona Enter...")

    elif opcion == "4":
        gastos = cargar_gastos(EXPENSES_FILE)
        periodo = input("📅 Ver: semanal (s) / mensual (m) [s]: ").strip().lower() or "s"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        print(f"\n{Fore.WHITE}📋 Últimos gastos del periodo:")
        for g in reversed(gastos_f[-8:]):
            print(f"  {Fore.GREEN}📅 {g['fecha']} | {g['categoria'].capitalize():<10} | {g['monto']:.2f}€ | {g['descripcion']}")
        input(f"{Fore.YELLOW}\nPresiona Enter...")

    elif opcion == "5":
        print(f"{Fore.CYAN}👋 ¡Hasta la próxima! Gestiona tu economía con inteligencia.")
        sys.exit(0)
    else:
        print(f"{Fore.RED}⚠️ Opción inválida. Elige 1-5.")