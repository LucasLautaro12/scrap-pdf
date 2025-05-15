import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_utils.extractor import extraer_datos_pdf

def cargar_pdf():
    ruta_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if ruta_pdf:
        datos = extraer_datos_pdf(ruta_pdf)
        messagebox.showinfo("Datos extraídos", datos)

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Lector de PDF")
    ventana.geometry("400x200")

    boton_cargar = tk.Button(ventana, text="Cargar PDF", command=cargar_pdf)
    boton_cargar.pack(expand=True)

    ventana.mainloop()
