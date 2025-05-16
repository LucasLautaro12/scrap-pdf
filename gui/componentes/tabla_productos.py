import tkinter as tk
from tkinter import ttk

class TablaProductos(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        columnas = ("tip", "cant", "ancho", "alto", "pxu", "ptotal")
        super().__init__(master, columns=columnas, show="headings", **kwargs)

        self.heading("tip", text="Tipología")
        self.heading("cant", text="Cantidad")
        self.heading("ancho", text="Ancho")
        self.heading("alto", text="Alto")
        self.heading("pxu", text="Precio x Unidad")
        self.heading("ptotal", text="Precio Total")

        self.column("tip", width=100)
        self.column("cant", width=70, anchor=tk.CENTER)
        self.column("ancho", width=80, anchor=tk.CENTER)
        self.column("alto", width=80, anchor=tk.CENTER)
        self.column("pxu", width=120, anchor=tk.E)
        self.column("ptotal", width=120, anchor=tk.E)

    def cargar_productos(self, productos):
        self.delete(*self.get_children())
        total = 0
        for prod in productos:
            self.insert("", tk.END, values=(
                prod['tipologia'],
                prod['cantidad'],
                prod['ancho'],
                prod['alto'],
                f"${prod['precio_unitario']:.2f}",
                f"${prod['total_producto']:.2f}"
            ))
            if prod['total_producto']:
                total += prod['total_producto']
        return total
