from pdf_utils.extractor import extraer_datos_pdf

ruta_pdf = "C:/Users/Usuario/Downloads/pdfs/19073 ACT 12-5-25 - COTIZACION VEXAR - DOS F ESTUDIO - CASA MM PVC.pdf"
productos = extraer_datos_pdf(ruta_pdf)

if not productos:
    print("⚠️ No se encontraron productos.")
else:
    print("✅ Productos extraídos:")
    for p in productos:
        print(p)
