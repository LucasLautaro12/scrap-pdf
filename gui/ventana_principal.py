""" import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_utils.extractor import extraer_datos_pdf
from pdf_utils.exportador_pdf import generar_pdf_comparativo
from tkinter import filedialog
import os
from gui.componentes.tabla_productos import TablaProductos
from tkinter import simpledialog

from pdf_utils.exportador_excel import generar_excel_comparativo


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

        self.btn_exportar = tk.Button(self.root, text="Exportar a PDF", command=self.exportar_pdf)
        self.btn_exportar.pack(pady=10)

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

    def exportar_pdf(self):
        if not self.productos_actual or not self.productos_anterior:
            messagebox.showwarning("Advertencia", "Cargá ambos PDFs antes de exportar.")
            return

        # Pedir datos al usuario
        cliente = simpledialog.askstring("Cliente", "Ingrese el nombre del cliente:")
        obra = simpledialog.askstring("Obra", "Ingrese el nombre de la obra:")
        ticket = simpledialog.askstring("Ticket Vexar", "Ingrese el número de ticket:")

        if not cliente or not obra or not ticket:
            messagebox.showwarning("Faltan datos", "Debe ingresar Cliente, Obra y Ticket.")
            return

        ruta_salida = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if ruta_salida:
            try:
                generar_pdf_comparativo(
                    ruta_salida,
                    self.productos_anterior,
                    self.productos_actual,
                    self.total_anterior,
                    self.total_actual,
                    cliente=cliente,
                    obra=obra,
                    ticket=ticket
                )
                messagebox.showinfo("Éxito", f"PDF generado en:\n{ruta_salida}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

    def exportar_excel(self):
        if not self.productos_actual or not self.productos_anterior:
            messagebox.showwarning("Advertencia", "Cargá ambos PDFs antes de exportar.")
            return

        cliente = simpledialog.askstring("Cliente", "Ingrese el nombre del cliente:")
        obra = simpledialog.askstring("Obra", "Ingrese el nombre de la obra:")
        ticket = simpledialog.askstring("Ticket Vexar", "Ingrese el número de ticket:")

        if not cliente or not obra or not ticket:
            messagebox.showwarning("Faltan datos", "Debe ingresar Cliente, Obra y Ticket.")
            return

        ruta_salida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if ruta_salida:
            try:
                generar_excel_comparativo(
                    ruta_salida,
                    self.productos_anterior,
                    self.productos_actual,
                    self.total_anterior,
                    self.total_actual,
                    cliente=cliente,
                    obra=obra,
                    ticket=ticket
                )
                messagebox.showinfo("Éxito", f"Excel generado en:\n{ruta_salida}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el Excel:\n{e}")

def iniciar_app():
    root = tk.Tk()
    app = ComparadorPDF(root)
    root.mainloop()
 """
 
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_utils.extractor import extraer_datos_pdf
from gui.componentes.tabla_productos import TablaProductos

from pdf_utils.exportador_excel import generar_excel_comparativo


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

        self.btn_exportar = tk.Button(self.root, text="Exportar a Excel", command=self.exportar_excel)
        self.btn_exportar.pack(pady=10)

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

    def exportar_excel(self):
        if not self.productos_actual or not self.productos_anterior:
            messagebox.showwarning("Advertencia", "Cargá ambos PDFs antes de exportar.")
            return

        ruta_salida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if ruta_salida:
            try:
                generar_excel_comparativo(
                    ruta_salida,
                    self.productos_anterior,
                    self.productos_actual,
                    self.total_anterior,
                    self.total_actual
                )
                messagebox.showinfo("Éxito", f"Excel generado en:\n{ruta_salida}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el Excel:\n{e}")


def iniciar_app():
    root = tk.Tk()
    app = ComparadorPDF(root)
    root.mainloop()
