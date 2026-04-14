"""
console_menu.py
Interfaz principal CRUD. Menú reordenado, tabla en ventana interactiva y flujo validado.
"""
import sys
import os
from colorama import init, Fore, Style
init(autoreset=True)

# Ruta raíz del proyecto para imports seguros
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import EXPENSES_FILE, DEFAULT_CATEGORIES, REPORTS_DIR
from data.storage import cargar_gastos, exportar_txt
from utils.validators import validar_monto, validar_categoria, validar_fecha
from core.expense_manager import (
    agregar_gasto, editar_gasto, eliminar_gasto,
    resumen_por_categoria, filtrar_por_periodo, generar_reporte
)
from ui.visualizer import generar_grafico
from ui.tabla_window import mostrar_ventana_tabla

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print(f"\n{Fore.CYAN}╔{'═'*50}╗")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}💶 GESTOR DE GASTOS ESTUDIANTIL (CRUD) 💶{Fore.CYAN}{' '*(10)}║")
    print(f"{Fore.CYAN}╠{'═'*50}╣")
    print(f"{Fore.WHITE}║  1. 📋 Ver lista completa               {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  2. ➕ Registrar nuevo gasto            {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  3. ✏️ Editar gasto existente           {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  4. 🗑️ Eliminar gasto                  {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  5. 📊 Resumen + Gráfico visual         {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  6. 💾 Exportar resumen a TXT           {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  7. 📅 Filtrar por periodo              {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  8. 🚪 Salir                            {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚{'═'*50}╝")

def solicitar_id_valido(gastos: list) -> int:
    while True:
        try:
            val = int(input(f"{Fore.WHITE}🔢 Introduce el ID del gasto: {Fore.RESET}").strip())
            if any(g["id"] == val for g in gastos):
                return val
            print(f"{Fore.RED}⚠️ ID no encontrado. Verifica la lista.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Debe ser un número entero.{Style.RESET_ALL}")

def ejecutar_opcion(opcion: str, presupuesto_mensual: float = None):
    gastos = cargar_gastos(EXPENSES_FILE)
    
    if opcion == "1":
        mostrar_ventana_tabla(gastos)
        input(f"\n{Fore.YELLOW}Presiona Enter cuando cierres la ventana para volver al menú...")

    elif opcion == "2":
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
        print(f"{Fore.GREEN if ok else Fore.RED}{msg}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Presiona Enter para continuar...")

    elif opcion == "3":
        if not gastos:
            print(f"{Fore.YELLOW}📭 No hay gastos para editar.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Presiona Enter..."); return
        mostrar_ventana_tabla(gastos)
        id_gasto = solicitar_id_valido(gastos)
        print(f"\n{Fore.CYAN}¿Qué campo deseas modificar?")
        print(f"{Fore.WHITE}1. 💰 Monto | 2. 📂 Categoría | 3. 📝 Descripción | 4. 📅 Fecha")
        campo_map = {"1": "monto", "2": "categoria", "3": "descripcion", "4": "fecha"}
        while True:
            op = input(f"{Fore.WHITE}👉 Elige opción (1-4): {Fore.RESET}").strip()
            if op in campo_map: break
            print(f"{Fore.RED}⚠️ Opción no válida.{Style.RESET_ALL}")
        
        campo = campo_map[op]
        if campo == "monto":
            while True:
                val, err = validar_monto(input("💰 Nuevo monto: ").strip())
                if err: print(f"{Fore.RED}❌ {err}")
                else: break
        elif campo == "categoria":
            while True:
                val, err = validar_categoria(input(f"📂 Nueva categoría: ").strip(), DEFAULT_CATEGORIES)
                if err: print(f"{Fore.RED}❌ {err}")
                else: break
        elif campo == "fecha":
            while True:
                val, err = validar_fecha(input("📅 Nueva fecha (YYYY-MM-DD): ").strip())
                if err: print(f"{Fore.RED}❌ {err}")
                else: break
        else:
            val = input("📝 Nueva descripción: ").strip()
            
        ok, msg = editar_gasto(EXPENSES_FILE, id_gasto, campo, val)
        print(f"{Fore.GREEN if ok else Fore.RED}{msg}{Style.RESET_ALL}")
        input(f"{Fore.YELLOW}Presiona Enter...")

    elif opcion == "4":
        if not gastos:
            print(f"{Fore.YELLOW}📭 No hay gastos para eliminar.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Presiona Enter..."); return
        mostrar_ventana_tabla(gastos)
        id_gasto = solicitar_id_valido(gastos)
        while True:
            conf = input(f"{Fore.RED}⚠️ ¿Estás seguro de eliminar el gasto #{id_gasto}? (s/n): {Fore.RESET}").strip().lower()
            if conf in ("s", "n"): break
            print(f"{Fore.RED}⚠️ Responde 's' o 'n'.{Style.RESET_ALL}")
        if conf == "s":
            ok, msg = eliminar_gasto(EXPENSES_FILE, id_gasto)
            print(f"{Fore.GREEN if ok else Fore.RED}{msg}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}✅ Operación cancelada.{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Presiona Enter...")

    elif opcion == "5":
        periodo = input("📅 Periodo: semanal (s) / mensual (m) [m]: ").strip().lower() or "m"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        resumen = resumen_por_categoria(gastos_f)
        total = sum(resumen.values())
        limpiar_pantalla()
        print(generar_reporte(resumen, total, presupuesto_mensual))
        generar_grafico(resumen)
        input(f"\n{Fore.YELLOW}Presiona Enter cuando cierres el gráfico...")

    elif opcion == "6":
        periodo = input("📅 Exportar: semanal (s) / mensual (m) [m]: ").strip().lower() or "m"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        resumen = resumen_por_categoria(gastos_f)
        total = sum(resumen.values())
        txt = generar_reporte(resumen, total, presupuesto_mensual)
        tipo = "semanal" if periodo=="s" else "mensual"
        ruta = os.path.join(REPORTS_DIR, f"gastos_{tipo}.txt")
        if exportar_txt(ruta, txt):
            print(f"{Fore.GREEN}✅ Exportado a: {ruta}")
        input(f"\n{Fore.YELLOW}Presiona Enter...")

    elif opcion == "7":
        periodo = input("📅 Ver: semanal (s) / mensual (m) [s]: ").strip().lower() or "s"
        gastos_f = filtrar_por_periodo(gastos, "semanal" if periodo=="s" else "mensual")
        print(f"\n{Fore.WHITE}📋 Gastos del periodo seleccionado:")
        mostrar_ventana_tabla(gastos_f)
        input(f"\n{Fore.YELLOW}Presiona Enter cuando cierres la ventana...")

    elif opcion == "8":
        print(f"{Fore.CYAN}👋 ¡Hasta la próxima! Gestiona tu economía con inteligencia.")
        sys.exit(0)
    else:
        print(f"{Fore.RED}⚠️ Opción inválida. Elige 1-8.")