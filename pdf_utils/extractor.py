import pdfplumber
import re

def procesar_precio(texto_precio):
    if not texto_precio:
        return None
    texto = texto_precio.strip()

    if ',' in texto and '.' in texto:
        ultima_coma = texto.rfind(',')
        ultima_punto = texto.rfind('.')
        if ultima_punto > ultima_coma:
            texto = texto.replace(',', '')
        else:
            texto = texto.replace('.', '').replace(',', '.')
    elif texto.count(',') == 1 and texto.count('.') == 0:
        texto = texto.replace(',', '.')
    else:
        texto = texto.replace(',', '').replace('.', '')

    try:
        return float(texto)
    except Exception as e:
        print(f"Error convirtiendo precio '{texto_precio}': {e}")
        return None

def extraer_datos_pdf(ruta_pdf):
    productos = []

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages[1:]:
            texto = pagina.extract_text()
            """ print("Leyendo página:", pagina.page_number)
            if texto:
                print("Texto extraído:\n", texto[:1000])
            else:
                print("⚠️ No se extrajo texto en esta página.")
                continue """

            # Buscamos líneas con: TIPOVALOR CANTIDAD MEDIDA (ANCHO x ALTO) PRECIO_UNIT TOTAL
            patron = re.compile(
                r"([A-Z]+\d+)\s+(\d+)\s+(\d+)\s*[xX]\s*(\d+)\s+([\d.,]+)\s+[\d.,]+"
            )

            for match in patron.finditer(texto):
                tipologia = match.group(1)
                cantidad = int(match.group(2))
                ancho = int(match.group(3))
                alto = int(match.group(4))
                precio_unitario = procesar_precio(match.group(5))

                productos.append({
                    "tipologia": tipologia,
                    "cantidad": cantidad,
                    "ancho": ancho,
                    "alto": alto,
                    "precio_unitario": precio_unitario,
                })

    return productos
