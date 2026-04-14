"""
table_window.py
Abre una ventana interactiva con Tkinter para visualizar los gastos en formato tabla profesional.
"""
import tkinter as tk
from tkinter import ttk

def mostrar_ventana_tabla(gastos: list):
    """
    Genera y muestra una ventana con tabla de gastos.
    Bloquea la ejecución hasta que el usuario cierra la ventana.
    """
    if not gastos:
        print("⚠️ No hay registros para mostrar.")
        return

    root = tk.Tk()
    root.title("💶 Gestor de Gastos - Listado Completo")
    root.geometry("850x420")
    root.resizable(False, False)
    root.iconify()  # Parpadea en barra de tareas para llamar atención

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    # Configuración de columnas
    columns = ("id", "fecha", "categoria", "monto", "descripcion")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

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

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Insertar datos
    for g in gastos:
        tree.insert("", tk.END, values=(
            g["id"], 
            g["fecha"], 
            g["categoria"].capitalize(), 
            f"{g['monto']:.2f}", 
            g["descripcion"]
        ))

    # Estilo visual profesional
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, borderwidth=1)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), foreground="#2c3e50")
    style.map("Treeview", background=[('selected', '#3498db')])

    # Cerrar ventana y liberar consola
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.deiconify()  # Trae la ventana al frente
    root.mainloop()