"""
ventana_tabla.py
Abre una ventana con Tkinter para visualizar una tabla, barra de estado financiero 
y estilo visual coherente con el proyecto.
"""
import tkinter as tk
from tkinter import ttk
from utilidades.formateadores import formato_fecha_display

def mostrar_ventana_tabla(gastos: list, presupuesto: float = None, total_gastado: float = 0.0):
    """
    Crea y muestra una ventana modal para visualizar el historial de gastos.
    Incluye barra superior con el estado del presupuesto y bloquea la ejecución
    hasta que el usuario cierra la ventana.
    """
    if not gastos and presupuesto is None:
        print("⚠️ No hay registros para mostrar.")
        return

    # Configuración inicial de la ventana principal
    root = tk.Tk()
    root.title("💶 Gestor de Gastos - Listado Completo")
    root.geometry("900x480")
    root.resizable(False, False)
    root.iconify()  # Parpadea en barra de tareas para llamar atención
    
    # Barra de estado financiero (visible solo si hay presupuesto configurado)
    if presupuesto is not None:
        dif = presupuesto - total_gastado
        status_txt = f"Presupuesto: {presupuesto:,.2f}€ | Gastado: {total_gastado:,.2f}€ | {'Restante' if dif>=0 else 'Déficit'}: {abs(dif):,.2f}€"
        color = "green" if dif >= 0 else "red"
        frame_status = ttk.Frame(root)
        frame_status.pack(fill="x", padx=10, pady=5)
        lbl_status = ttk.Label(frame_status, text=status_txt, font=("Segoe UI", 11, "bold"), foreground=color)
        lbl_status.pack()

    # Marco principal y configuración de la tabla (Treeview)
    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    # Configuración de columnas
    columns = ("id", "fecha", "categoria", "monto", "descripcion")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

    # Definición de cabeceras y anchos de columna
    tree.heading("id", text="ID")
    tree.heading("fecha", text="Fecha")
    tree.heading("categoria", text="Categoría")
    tree.heading("monto", text="Monto (€)")
    tree.heading("descripcion", text="Descripción")

    tree.column("id", width=50, anchor="center")
    tree.column("fecha", width=90, anchor="center")
    tree.column("categoria", width=110, anchor="center")
    tree.column("monto", width=90, anchor="center")
    tree.column("descripcion", width=400, anchor="w")

    # Integración de barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Poblado de la tabla con los datos formateados
    for g in gastos:
        tree.insert("", tk.END, values=(
            g["id"], 
            formato_fecha_display(g["fecha"]),
            g["categoria"].capitalize(), 
            f"{g['monto']:.2f}", 
            g["descripcion"]
        ))

    # Aplicación de estilo visual profesional 
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, borderwidth=1)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground="#2c3e50")
    style.map("Treeview", background=[('selected', '#3498db')])

    # Cerrar ventana y liberar consola
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.deiconify()  # Trae la ventana al frente
    root.mainloop()