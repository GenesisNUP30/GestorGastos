"""
core/expense_manager.py
Lógica de negocio: CRUD completo, cálculo de resúmenes, filtrado temporal y reportes.
"""
import os
from datetime import datetime, timedelta
from utils.formatters import formato_moneda
from data.storage import cargar_gastos, guardar_gastos

def agregar_gasto(ruta_archivo: str, monto: float, categoria: str, descripcion: str, fecha: str) -> tuple:
    gastos = cargar_gastos(ruta_archivo)
    # Genera ID único incluso si se han borrado registros intermedios
    nuevo_id = max((g["id"] for g in gastos), default=0) + 1
    nuevo = {
        "id": nuevo_id,
        "monto": monto,
        "categoria": categoria.lower(),
        "descripcion": descripcion,
        "fecha": fecha
    }
    gastos.append(nuevo)
    if guardar_gastos(ruta_archivo, gastos):
        return True, f"✅ Gasto #{nuevo_id} registrado correctamente."
    return False, "❌ Error al registrar el gasto."

def editar_gasto(ruta_archivo: str, id_gasto: int, campo: str, nuevo_valor) -> tuple:
    """Modifica un campo específico de un gasto existente."""
    gastos = cargar_gastos(ruta_archivo)
    for g in gastos:
        if g["id"] == id_gasto:
            if campo == "monto":
                g["monto"] = float(nuevo_valor)
            elif campo == "categoria":
                g["categoria"] = str(nuevo_valor).lower()
            elif campo == "descripcion":
                g["descripcion"] = str(nuevo_valor)
            elif campo == "fecha":
                g["fecha"] = str(nuevo_valor)
            if guardar_gastos(ruta_archivo, gastos):
                return True, f"✅ Gasto #{id_gasto} actualizado correctamente."
            return False, "❌ Error al guardar los cambios."
    return False, f"❌ No se encontró el gasto con ID #{id_gasto}."

def eliminar_gasto(ruta_archivo: str, id_gasto: int) -> tuple:
    """Elimina un gasto por su ID y reordena la persistencia."""
    gastos = cargar_gastos(ruta_archivo)
    gastos_filtrados = [g for g in gastos if g["id"] != id_gasto]
    if len(gastos_filtrados) == len(gastos):
        return False, f"❌ No se encontró el gasto con ID #{id_gasto}."
    if guardar_gastos(ruta_archivo, gastos_filtrados):
        return True, f"🗑️ Gasto #{id_gasto} eliminado correctamente."
    return False, "❌ Error al eliminar el gasto."

def resumen_por_categoria(gastos: list) -> dict:
    resumen = {}
    for g in gastos:
        resumen[g["categoria"]] = resumen.get(g["categoria"], 0.0) + g["monto"]
    return resumen

def filtrar_por_periodo(gastos: list, periodo: str) -> list:
    hoy = datetime.now().date()
    if periodo == "semanal":
        inicio = hoy - timedelta(days=hoy.weekday())
    else:
        inicio = hoy.replace(day=1)
    return [g for g in gastos if datetime.strptime(g["fecha"], "%Y-%m-%d").date() >= inicio]

def generar_reporte(resumen: dict, total: float, presupuesto: float = None) -> str:
    lineas = ["📊 RESUMEN VISUAL DE GASTOS", "="*45]
    for cat, monto in sorted(resumen.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (monto / total * 100) if total > 0 else 0
        barra = "█" * int(porcentaje / 5) + "░" * (20 - int(porcentaje / 5))
        estado = "🟢" if (presupuesto and monto <= presupuesto/len(resumen)) else "🟡"
        lineas.append(f"{estado} {cat.capitalize():<12} {barra} {formato_moneda(monto)} ({porcentaje:.1f}%)")
    lineas.extend(["="*45, f"💰 TOTAL: {formato_moneda(total)}"])
    if presupuesto:
        lineas.append(f"📅 Restante mensual: {formato_moneda(presupuesto - total)}")
    return "\n".join(lineas)