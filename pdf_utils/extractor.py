import pdfplumber

def extraer_datos_pdf(ruta_pdf):
    datos_extraidos = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                datos_extraidos.append(texto)

    # Aquí podés aplicar regex o lógica para extraer solo lo importante
    # Por ahora, devolvemos los primeros 500 caracteres como muestra
    texto_completo = "\n".join(datos_extraidos)
    return texto_completo[:500] + "..." if len(texto_completo) > 500 else texto_completo
