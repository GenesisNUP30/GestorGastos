"""
menu_consola.py
Interfaz CRUD. Menú reordenado, alertas de presupuesto en tiempo real y opción para modificarlo.
"""
import sys
import os
import re
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import EXPENSES_FILE, CONFIG_FILE, DEFAULT_CATEGORIES, REPORTS_DIR
from datos.almacenamiento import cargar_gastos, exportar_txt, cargar_configuracion, guardar_configuracion
from utilidades.validadores import validar_monto, validar_categoria, validar_fecha
from utilidades.formateadores import formato_moneda
from nucleo.gestor_gastos import (
    agregar_gasto, editar_gasto, eliminar_gasto,
    resumen_por_categoria, filtrar_por_mes, generar_reporte
)
from interfaz.visualizador import generar_grafico
from interfaz.ventana_tabla import mostrar_ventana_tabla


def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    print(f"\n{Fore.CYAN}╔{'═' * 50}╗")
    print(f"{Fore.CYAN}║ {Fore.YELLOW}💶 GESTOR DE GASTOS ESTUDIANTIL (CRUD) 💶{Fore.CYAN}{' ' * 10}║")
    print(f"{Fore.CYAN}╠{'═' * 50}╣")
    print(f"{Fore.WHITE}║  1. 📋 Ver lista completa               {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  2. ➕ Registrar nuevo gasto            {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  3. ✏️ Editar gasto existente           {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  4. 🗑️ Eliminar gasto                  {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  5. 📊 Resumen + Gráfico visual         {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  6. 💾 Exportar resumen a TXT           {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  7. 📅 Filtrar por mes/año              {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  8. 💰 Configurar/Cambiar presupuesto   {Fore.CYAN}║")
    print(f"{Fore.WHITE}║  9. 🚪 Salir                            {Fore.CYAN}║")
    print(f"{Fore.CYAN}╚{'═' * 50}╝")


def solicitar_mes() -> str:
    hoy = datetime.now().strftime("%Y-%m")
    mes = input(f"{Fore.WHITE}📅 Mes/Año (YYYY-MM) o [Enter] para {hoy}: {Fore.RESET}").strip()
    if not mes:
        return hoy
    if not re.match(r"^\d{4}-\d{2}$", mes):
        print(f"{Fore.RED}⚠️ Formato inválido. Usa YYYY-MM (ej: 2024-10).{Style.RESET_ALL}")
        return solicitar_mes()
    return mes


def obtener_presupuesto(mes: str) -> float | None:
    config = cargar_configuracion(CONFIG_FILE)
    presupuestos = config.get("presupuestos", {})
    if mes in presupuestos:
        return float(presupuestos[mes])

    while True:
        val = input(
            f"{Fore.WHITE}💰 Sin presupuesto para {mes}. Introduce uno (€) o [Enter] para ilimitado: {Fore.RESET}"
        ).strip()
        if not val:
            return None
        try:
            pres = float(val.replace(",", "."))
            if pres <= 0:
                raise ValueError
            presupuestos[mes] = pres
            config["presupuestos"] = presupuestos
            guardar_configuracion(CONFIG_FILE, config)
            print(f"{Fore.GREEN}✅ Presupuesto guardado para {mes}.{Style.RESET_ALL}")
            return pres
        except ValueError:
            print(f"{Fore.RED}❌ Número inválido o <= 0.{Style.RESET_ALL}")


def cambiar_presupuesto():
    """Permite modificar o establecer el presupuesto de cualquier mes."""
    mes = solicitar_mes()
    config = cargar_configuracion(CONFIG_FILE)
    presupuestos = config.get("presupuestos", {})
    actual = presupuestos.get(mes)

    if actual is not None:
        print(f"{Fore.CYAN}📌 Presupuesto actual para {mes}: {actual:.2f}€{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Deja vacío para mantenerlo o introduce un nuevo valor.{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}📌 No hay presupuesto configurado para {mes}.{Style.RESET_ALL}")

    while True:
        val = input(f"{Fore.WHITE}💰 Nuevo presupuesto (€) o [Enter] para cancelar: {Fore.RESET}").strip()
        if not val:
            print(f"{Fore.YELLOW}⚠️ Operación cancelada.{Style.RESET_ALL}")
            return
        try:
            nuevo = float(val.replace(",", "."))
            if nuevo <= 0:
                raise ValueError
            presupuestos[mes] = nuevo
            config["presupuestos"] = presupuestos
            guardar_configuracion(CONFIG_FILE, config)
            print(f"{Fore.GREEN}✅ Presupuesto actualizado para {mes}: {nuevo:.2f}€{Style.RESET_ALL}")
            return
        except ValueError:
            print(f"{Fore.RED}❌ Introduce un número válido mayor a 0.{Style.RESET_ALL}")


def mostrar_alerta_presupuesto(mes: str):
    """Calcula y muestra el estado financiero del mes. Nunca bloquea."""
    config = cargar_configuracion(CONFIG_FILE)
    presupuesto = config.get("presupuestos", {}).get(mes)
    gastos = cargar_gastos(EXPENSES_FILE)
    total = sum(g["monto"] for g in gastos if g["fecha"].startswith(mes))

    if presupuesto is None:
        msg = f"📊 Mes {mes}: Gastado {formato_moneda(total)} | Presupuesto: Ilimitado"
        color = Fore.CYAN
    else:
        dif = presupuesto - total
        if dif >= 0:
            msg = (
                f"✅ Mes {mes}: Presupuesto {formato_moneda(presupuesto)} | "
                f"Gastado {formato_moneda(total)} | Restante {formato_moneda(dif)}"
            )
            color = Fore.GREEN
        else:
            msg = (
                f"🚨 ALERTA Mes {mes}: Presupuesto {formato_moneda(presupuesto)} | "
                f"Gastado {formato_moneda(total)} | Déficit {formato_moneda(abs(dif))}"
            )
            color = Fore.RED
    print(f"{color}{msg}{Style.RESET_ALL}")


def solicitar_id_valido(gastos: list) -> int:
    while True:
        try:
            val = int(input(f"{Fore.WHITE}🔢 ID del gasto: {Fore.RESET}").strip())
            if any(g["id"] == val for g in gastos):
                return val
            print(f"{Fore.RED}⚠️ ID no encontrado.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Introduce un número entero.{Style.RESET_ALL}")


def ejecutar_opcion(opcion: str):
    mes_actual = datetime.now().strftime("%Y-%m")

    if opcion == "1":
        mostrar_alerta_presupuesto(mes_actual)
        gastos = cargar_gastos(EXPENSES_FILE)
        config = cargar_configuracion(CONFIG_FILE)
        pres = config.get("presupuestos", {}).get(mes_actual)
        total = sum(g["monto"] for g in gastos if g["fecha"].startswith(mes_actual))
        mostrar_ventana_tabla(gastos, presupuesto=pres, total_gastado=total)
        input(f"\n{Fore.YELLOW}Cierra la ventana y presiona Enter...")

    elif opcion == "2":
        while True:
            monto, err = validar_monto(input("💰 Monto (ej: 15.50): ").strip())
            if err:
                print(f"{Fore.RED}❌ {err}")
            else:
                break
        while True:
            cat, err = validar_categoria(
                input(f"📂 Categoría ({', '.join(DEFAULT_CATEGORIES)}): ").strip(),
                DEFAULT_CATEGORIES
            )
            if err:
                print(f"{Fore.RED}❌ {err}")
            else:
                break
        desc = input("📝 Descripción (Enter=ninguna): ").strip() or "Sin descripción"
        while True:
            fecha_input = input("📅 Fecha (YYYY-MM-DD, Enter=hoy): ").strip()
            if not fecha_input:
                fecha_input = datetime.now().strftime("%Y-%m-%d")
            fecha, err = validar_fecha(fecha_input)
            if err:
                print(f"{Fore.RED}❌ {err}")
            else:
                break
        ok, msg = agregar_gasto(EXPENSES_FILE, monto, cat, desc, fecha)
        print(f"{Fore.GREEN if ok else Fore.RED}{msg}{Style.RESET_ALL}")
        mostrar_alerta_presupuesto(fecha[:7])
        input(f"{Fore.YELLOW}Presiona Enter...")

    elif opcion == "3":
        gastos = cargar_gastos(EXPENSES_FILE)
        if not gastos:
            print(f"{Fore.YELLOW}📭 No hay gastos.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Presiona Enter...")
            return
        mostrar_ventana_tabla(gastos)
        id_gasto = solicitar_id_valido(gastos)
        print(f"{Fore.WHITE}1. 💰 Monto | 2. 📂 Categoría | 3. 📝 Descripción | 4. 📅 Fecha")
        campo_map = {"1": "monto", "2": "categoria", "3": "descripcion", "4": "fecha"}
        while True:
            op = input(f"{Fore.WHITE}👉 Elige (1-4): {Fore.RESET}").strip()
            if op in campo_map:
                break
            print(f"{Fore.RED}⚠️ Opción inválida.{Style.RESET_ALL}")
        campo = campo_map[op]
        if campo == "monto":
            while True:
                val, err = validar_monto(input("💰 Nuevo monto: ").strip())
                if err:
                    print(f"{Fore.RED}❌ {err}")
                else:
                    break
        elif campo == "categoria":
            while True:
                val, err = validar_categoria(
                    input("📂 Nueva categoría: ").strip(),
                    DEFAULT_CATEGORIES
                )
                if err:
                    print(f"{Fore.RED}❌ {err}")
                else:
                    break
        elif campo == "fecha":
            while True:
                val, err = validar_fecha(input("📅 Nueva fecha (YYYY-MM-DD): ").strip())
                if err:
                    print(f"{Fore.RED}❌ {err}")
                else:
                    break
        else:
            val = input("📝 Nueva descripción: ").strip()
        ok, msg = editar_gasto(EXPENSES_FILE, id_gasto, campo, val)
        print(f"{Fore.GREEN if ok else Fore.RED}{msg}{Style.RESET_ALL}")
        mostrar_alerta_presupuesto(mes_actual)
        input()

    elif opcion == "4":
        gastos = cargar_gastos(EXPENSES_FILE)
        if not gastos:
            print(f"{Fore.YELLOW}📭 No hay gastos.{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Presiona Enter...")
            return
        mostrar_ventana_tabla(gastos)
        id_gasto = solicitar_id_valido(gastos)
        while True:
            conf = input(f"{Fore.RED}⚠️ ¿Eliminar #{id_gasto}? (s/n): {Fore.RESET}").strip().lower()
            if conf in ("s", "n"):
                break
        if conf == "s":
            ok, msg = eliminar_gasto(EXPENSES_FILE, id_gasto)
            print(f"{Fore.GREEN if ok else Fore.RED}{msg}{Style.RESET_ALL}")
        mostrar_alerta_presupuesto(mes_actual)
        input()

    elif opcion in ("5", "6", "7"):
        mes = solicitar_mes()
        presupuesto = obtener_presupuesto(mes)
        gastos_mes = filtrar_por_mes(cargar_gastos(EXPENSES_FILE), mes)
        resumen = resumen_por_categoria(gastos_mes)
        total = sum(resumen.values())
        reporte = generar_reporte(resumen, total, mes, presupuesto)

        if opcion == "5":
            limpiar_pantalla()
            print(reporte)
            generar_grafico(resumen)
        elif opcion == "6":
            ruta = os.path.join(REPORTS_DIR, f"gastos_{mes}.txt")
            if exportar_txt(ruta, reporte):
                print(f"{Fore.GREEN}✅ Exportado a: {ruta}")
        else:
            print(f"\n{Fore.WHITE}📋 Gastos registrados en {mes}:")
            mostrar_ventana_tabla(gastos_mes, presupuesto=presupuesto, total_gastado=total)
        input(f"\n{Fore.YELLOW}Presiona Enter...")

    elif opcion == "8":
        cambiar_presupuesto()
        input(f"{Fore.YELLOW}Presiona Enter para continuar...")

    elif opcion == "9":
        print(f"{Fore.CYAN}👋 ¡Hasta la próxima! Gestiona tu economía con inteligencia.")
        sys.exit(0)
    else:
        print(f"{Fore.RED}⚠️ Opción inválida. Elige 1-9.")