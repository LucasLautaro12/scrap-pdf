import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pdf_utils.extractor import extraer_datos_pdf

def cargar_pdf(campo_texto):
    ruta_pdf = filedialog.askopenfilename(filetypes=[("Archivos PDF", "*.pdf")])
    if ruta_pdf:
        try:
            productos = extraer_datos_pdf(ruta_pdf)
            if not productos:
                campo_texto.delete("1.0", tk.END)
                campo_texto.insert(tk.END, "⚠️ No se encontraron productos.")
            else:
                campo_texto.delete("1.0", tk.END)
                for i, prod in enumerate(productos, 1):
                    texto = f"{i}. Tipología: {prod['tipologia']}\n"
                    texto += f"   Cantidad: {prod['cantidad']}\n"
                    texto += f"   Ancho: {prod['ancho']}\n"
                    texto += f"   Alto: {prod['alto']}\n"
                    texto += f"   Precio x Unidad: ${prod['precio_unitario']:.2f}\n\n"
                    campo_texto.insert(tk.END, texto)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error procesando el PDF:\n{str(e)}")

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Extractor de Productos PDF")
    ventana.geometry("600x500")

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    boton_cargar = tk.Button(frame_botones, text="Cargar PDF", command=lambda: cargar_pdf(campo_texto))
    boton_cargar.pack()

    campo_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=70, height=25)
    campo_texto.pack(padx=10, pady=10, expand=True, fill="both")

    ventana.mainloop()

