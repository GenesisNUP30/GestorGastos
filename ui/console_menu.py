"""
console_menu.py
Interfaz principal. Maneja el flujo de usuario, validaciones y llamadas a la lógica.
"""
import sys
import os
from colorama import init, Fore, Style
init(autoreset=True)

from config import EXPENSES_FILE, DEFAULT_CATEGORIES, REPORTS_DIR, EXPORT_FILENAME
from data.storage import cargar_gastos, exportar_txt
from utils.validators import validar_monto, validar_categoria, validar_fecha
from core.expense_manager import agregar_gasto, resumen_por_categoria, filtrar_por_periodo, generar_reporte
from ui.visualizer import generar_grafico

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.YELLOW}💶 GESTOR DE GASTOS ESTUDIANTIL 💶")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.WHITE}1. ➕ Registrar nuevo gasto")
    print(f"{Fore.WHITE}2. 📋 Ver lista completa de gastos")
    print(f"{Fore.WHITE}3. 📊 Ver resumen + Gráfico visual")
    print(f"{Fore.WHITE}4. 💾 Exportar resumen a TXT")
    print(f"{Fore.WHITE}5. 📅 Filtrar por periodo")
    print(f"{Fore.WHITE}6. 🚪 Salir")
    print(f"{Fore.CYAN}{'='*50}")

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
        if not gastos:
            print(f"{Fore.YELLOW}📭 No hay gastos registrados aún.{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.CYAN}{'='*65}")
            print(f"{Fore.YELLOW}📋 HISTORIAL COMPLETO DE GASTOS (Más recientes primero)")
            print(f"{Fore.CYAN}{'='*65}")
            print(f"{Fore.WHITE}{'ID':<4} | {'FECHA':<12} | {'CATEGORÍA':<12} | {'MONTO':<10} | {'DESCRIPCIÓN'}")
            print(f"{Fore.CYAN}{'-'*65}")
            # Muestra los últimos 30 para no saturar la terminal
            limite = 30
            mostrar = gastos[-limite:]
            for g in reversed(mostrar):
                print(f"{Fore.WHITE}{g['id']:<4} | {g['fecha']:<12} | {g['categoria'].capitalize():<12} | {g['monto']:<10.2f}€ | {g['descripcion']}")
            if len(gastos) > limite:
                print(f"{Fore.YELLOW}⚠️ Mostrando los {limite} más recientes de {len(gastos)} totales.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*65}")
        input(f"\n{Fore.YELLOW}Presiona Enter para volver al menú...")

    elif opcion == "3":
        gastos = cargar_gastos(EXPENSES_FILE)
        periodo = input("📅 Periodo: semanal (s) / mensual (m) [m]: ").strip().lower() or "m"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        resumen = resumen_por_categoria(gastos_f)
        total = sum(resumen.values())
        limpiar_pantalla()
        print(generar_reporte(resumen, total, presupuesto_mensual))
        generar_grafico(resumen)
        input(f"{Fore.YELLOW}\nPresiona Enter para continuar...")

    elif opcion == "4":
        gastos = cargar_gastos(EXPENSES_FILE)
        periodo = input("📅 Exportar: semanal (s) / mensual (m) [m]: ").strip().lower() or "m"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        resumen = resumen_por_categoria(gastos_f)
        total = sum(resumen.values())
        txt = generar_reporte(resumen, total, presupuesto_mensual)
        tipo = "semanal" if periodo=="s" else "mensual"
        ruta = os.path.join(REPORTS_DIR, f"gastos_{tipo}.txt")
        if exportar_txt(ruta, txt):
            print(f"{Fore.GREEN}✅ Exportado a: {ruta}")
        input(f"{Fore.YELLOW}\nPresiona Enter...")

    elif opcion == "5":
        gastos = cargar_gastos(EXPENSES_FILE)
        periodo = input("📅 Ver: semanal (s) / mensual (m) [s]: ").strip().lower() or "s"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        print(f"\n{Fore.WHITE}📋 Gastos del periodo seleccionado:")
        if not gastos_f:
            print(f"{Fore.YELLOW}No hay registros en este periodo.{Style.RESET_ALL}")
        else:
            for g in reversed(gastos_f[-10:]):
                print(f"  {Fore.GREEN}📅 {g['fecha']} | {g['categoria'].capitalize():<10} | {g['monto']:.2f}€ | {g['descripcion']}")
        input(f"{Fore.YELLOW}\nPresiona Enter...")

    elif opcion == "6":
        print(f"{Fore.CYAN}👋 ¡Hasta la próxima! Gestiona tu economía con inteligencia.")
        sys.exit(0)
    else:
        print(f"{Fore.RED}⚠️ Opción inválida. Elige 1-6.")