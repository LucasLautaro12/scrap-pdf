import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pdf_utils.extractor import extraer_datos_pdf
import os

def cargar_pdfs(campo_texto):
    rutas_pdf = filedialog.askopenfilenames(filetypes=[("Archivos PDF", "*.pdf")])
    if rutas_pdf:
        campo_texto.delete("1.0", tk.END)

        for ruta in rutas_pdf:
            nombre_archivo = os.path.basename(ruta)
            try:
                productos = extraer_datos_pdf(ruta)
                campo_texto.insert(tk.END, f"Archivo: {nombre_archivo}\n")
                campo_texto.insert(tk.END, "-" * 70 + "\n")

                if not productos:
                    campo_texto.insert(tk.END, "No se encontraron productos.\n\n")
                else:
                    for i, prod in enumerate(productos, 1):
                        texto = f"{i}. Tipología: {prod['tipologia']}\n"
                        texto += f"   Cantidad: {prod['cantidad']}\n"
                        texto += f"   Ancho: {prod['ancho']}\n"
                        texto += f"   Alto: {prod['alto']}\n"
                        texto += f"   Precio x Unidad: ${prod['precio_unitario']:.2f}\n"
                        texto += f"   Precio Total: ${prod['total_producto']:.2f}\n\n"
                        campo_texto.insert(tk.END, texto)
                campo_texto.insert(tk.END, "\n\n")


            except Exception as e:
                campo_texto.insert(tk.END, f"Error procesando {nombre_archivo}:\n{str(e)}\n\n")
        campo_texto.insert(tk.END, f"💰 TOTAL PRESUPUESTO GENERAL: ${prod['total_presupuesto']:,.2f}\n")

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Extractor de Productos PDF")
    ventana.geometry("700x550")

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    boton_cargar = tk.Button(frame_botones, text="Cargar PDF(s)", command=lambda: cargar_pdfs(campo_texto))
    boton_cargar.pack()

    campo_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=30)
    campo_texto.pack(padx=10, pady=10, expand=True, fill="both")

    ventana.mainloop()


