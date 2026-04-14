"""
expense_manager.py
Lógica de negocio: cálculo de resúmenes, filtrado temporal y generación de reportes.
"""
from datetime import datetime, timedelta
from utils.formatters import formato_moneda
from data.storage import cargar_gastos, guardar_gastos

def agregar_gasto(ruta_archivo: str, monto: float, categoria: str, descripcion: str, fecha: str) -> tuple:
    gastos = cargar_gastos(ruta_archivo)
    nuevo = {
        "id": len(gastos) + 1,
        "monto": monto,
        "categoria": categoria,
        "descripcion": descripcion,
        "fecha": fecha
    }
    gastos.append(nuevo)
    if guardar_gastos(ruta_archivo, gastos):
        return True, "✅ Gasto registrado correctamente."
    return False, "❌ Error al registrar."

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
    lineas = ["📊 RESUMEN VISUAL DE GASTOS", "="*40]
    for cat, monto in sorted(resumen.items(), key=lambda x: x[1], reverse=True):
        porcentaje = (monto / total * 100) if total > 0 else 0
        barra = "█" * int(porcentaje / 5) + "░" * (20 - int(porcentaje / 5))
        estado = "🟢" if (presupuesto and monto <= presupuesto/len(resumen)) else "🟡"
        lineas.append(f"{estado} {cat.capitalize():<10} {barra} {formato_moneda(monto)} ({porcentaje:.1f}%)")
    lineas.extend(["="*40, f"💰 TOTAL: {formato_moneda(total)}"])
    if presupuesto:
        lineas.append(f"📅 Restante mensual: {formato_moneda(presupuesto - total)}")
    return "\n".join(lineas)