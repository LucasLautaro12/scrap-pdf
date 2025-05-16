import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pdf_utils.extractor import extraer_datos_pdf
import os

def cargar_dos_pdfs(campo_texto):
    rutas_pdf = filedialog.askopenfilenames(filetypes=[("Archivos PDF", "*.pdf")])

    if not rutas_pdf or len(rutas_pdf) != 2:
        messagebox.showwarning("Atención", "Debes seleccionar exactamente 2 archivos PDF: uno anterior y uno actual.")
        return

    campo_texto.delete("1.0", tk.END)

    # Extraemos rutas y nombres
    ruta_anterior, ruta_actual = rutas_pdf
    nombre_anterior = os.path.basename(ruta_anterior)
    nombre_actual = os.path.basename(ruta_actual)

    try:
        productos_anterior = extraer_datos_pdf(ruta_anterior)
        productos_actual = extraer_datos_pdf(ruta_actual)
    except Exception as e:
        messagebox.showerror("Error", f"Error procesando uno de los archivos:\n{str(e)}")
        return

    # 🟡 Sección 1: Anterior
    campo_texto.insert(tk.END, f"📄 PRESUPUESTO ANTERIOR: {nombre_anterior}\n")
    campo_texto.insert(tk.END, "-" * 70 + "\n")
    total_anterior = 0

    if not productos_anterior:
        campo_texto.insert(tk.END, "⚠️ No se encontraron productos en el PDF anterior.\n\n")
    else:
        for i, prod in enumerate(productos_anterior, 1):
            texto = f"{i}. Tipología: {prod['tipologia']}\n"
            texto += f"   Cantidad: {prod['cantidad']}\n"
            texto += f"   Ancho: {prod['ancho']}\n"
            texto += f"   Alto: {prod['alto']}\n"
            texto += f"   Precio x Unidad: ${prod['precio_unitario']:.2f}\n"
            texto += f"   Precio Total: ${prod['total_producto']:.2f}\n\n"
            campo_texto.insert(tk.END, texto)

            if prod['total_producto']:
                total_anterior += prod['total_producto']

    campo_texto.insert(tk.END, f"🧮 Total Anterior: ${total_anterior:,.2f}\n\n\n")

    # 🟢 Sección 2: Actual
    campo_texto.insert(tk.END, f"📄 PRESUPUESTO ACTUAL: {nombre_actual}\n")
    campo_texto.insert(tk.END, "-" * 70 + "\n")
    total_actual = 0

    if not productos_actual:
        campo_texto.insert(tk.END, "⚠️ No se encontraron productos en el PDF actual.\n\n")
    else:
        for i, prod in enumerate(productos_actual, 1):
            texto = f"{i}. Tipología: {prod['tipologia']}\n"
            texto += f"   Cantidad: {prod['cantidad']}\n"
            texto += f"   Ancho: {prod['ancho']}\n"
            texto += f"   Alto: {prod['alto']}\n"
            texto += f"   Precio x Unidad: ${prod['precio_unitario']:.2f}\n"
            texto += f"   Precio Total: ${prod['total_producto']:.2f}\n\n"
            campo_texto.insert(tk.END, texto)

            if prod['total_producto']:
                total_actual += prod['total_producto']

    campo_texto.insert(tk.END, f"🧮 Total Actual: ${total_actual:,.2f}\n\n")

    # 💰 Comparación final
    diferencia = total_actual - total_anterior
    campo_texto.insert(tk.END, "=" * 70 + "\n")
    campo_texto.insert(
        tk.END,
        f"💰 DIFERENCIA TOTAL: {'🔺 Aumentó' if diferencia > 0 else '🔻 Disminuyó' if diferencia < 0 else '✅ Sin cambios'} "
        f"${abs(diferencia):,.2f}\n"
    )

def iniciar_app():
    ventana = tk.Tk()
    ventana.title("Comparador de Presupuestos PDF")
    ventana.geometry("800x650")

    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)

    boton_cargar = tk.Button(frame_botones, text="Cargar 2 PDFs (anterior y actual)", command=lambda: cargar_dos_pdfs(campo_texto))
    boton_cargar.pack()

    campo_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=95, height=35)
    campo_texto.pack(padx=10, pady=10, expand=True, fill="both")

    ventana.mainloop()
