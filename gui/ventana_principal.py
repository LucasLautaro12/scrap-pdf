import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pdf_utils.extractor import extraer_datos_pdf
import os
from gui.componentes.tabla_productos import TablaProductos

# app/gui/ventana_principal.py
class ComparadorPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Presupuestos PDF")
        self.root.geometry("1000x700")

        self.total_anterior = 0
        self.total_actual = 0
        self.productos_anterior = []
        self.productos_actual = []

        self.build_ui()

    def build_ui(self):
        frame_main = tk.Frame(self.root)
        frame_main.pack(pady=10, fill=tk.BOTH, expand=True)

        frame_izq = tk.LabelFrame(frame_main, text="PRESUPUESTO ANTERIOR", padx=10, pady=10)
        frame_der = tk.LabelFrame(frame_main, text="PRESUPUESTO ACTUAL", padx=10, pady=10)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        self.btn_anterior = tk.Button(frame_izq, text="Cargar PDF Anterior", command=self.cargar_pdf_anterior)
        self.btn_anterior.pack(pady=5)

        self.tree_anterior = TablaProductos(frame_izq, height=25)
        self.tree_anterior.pack(fill=tk.BOTH, expand=True)

        self.btn_actual = tk.Button(frame_der, text="Cargar PDF Actual", command=self.cargar_pdf_actual)
        self.btn_actual.pack(pady=5)

        self.tree_actual = TablaProductos(frame_der, height=25)
        self.tree_actual.pack(fill=tk.BOTH, expand=True)

        self.lbl_diferencia = tk.Label(self.root, text="DIFERENCIA TOTAL: ", font=("Arial", 12, "bold"))
        self.lbl_diferencia.pack(pady=10)

    def cargar_pdf_anterior(self):
        ruta = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if ruta:
            try:
                self.productos_anterior = extraer_datos_pdf(ruta)
                self.total_anterior = self.tree_anterior.cargar_productos(self.productos_anterior)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error con el PDF anterior:\n{str(e)}")
            self.actualizar_diferencia()

    def cargar_pdf_actual(self):
        ruta = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if ruta:
            try:
                self.productos_actual = extraer_datos_pdf(ruta)
                self.total_actual = self.tree_actual.cargar_productos(self.productos_actual)
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error con el PDF actual:\n{str(e)}")
            self.actualizar_diferencia()

    def actualizar_diferencia(self):
        if self.total_anterior == 0 and self.total_actual == 0:
            self.lbl_diferencia.config(text="DIFERENCIA TOTAL: Esperando archivos...")
            return

        diferencia = self.total_actual - self.total_anterior
        if diferencia > 0:
            texto = f"DIFERENCIA TOTAL: 🔺 El cliente debe pagar ${abs(diferencia):,.2f}"
        elif diferencia < 0:
            texto = f"DIFERENCIA TOTAL: 🔻 A favor del cliente ${abs(diferencia):,.2f}"
        else:
            texto = f"DIFERENCIA TOTAL: ✅ Sin cambios de monto"
        self.lbl_diferencia.config(text=texto)


def iniciar_app():
    root = tk.Tk()
    app = ComparadorPDF(root)
    root.mainloop()
