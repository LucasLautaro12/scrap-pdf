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
    total_presupuesto = 0
    presupuesto_nro = ""
    cliente = ""
    obra = ""

    with pdfplumber.open(ruta_pdf) as pdf:
        # Extraer datos de la primera página (índice 0)
        texto_primera = pdf.pages[0].extract_text()

        if texto_primera:
            match_pres = re.search(r"Presupuesto Nro:\s*(\d+)", texto_primera)
            match_cliente = re.search(r"Sres?\.\s*(.+)", texto_primera)
            match_obra = re.search(r"Ref\.\s*(.+)", texto_primera)

            if match_pres:
                presupuesto_nro = match_pres.group(1).strip()
            if match_cliente:
                cliente = match_cliente.group(1).strip()
            if match_obra:
                obra = match_obra.group(1).strip()

        # Extraer productos desde la segunda página
        for pagina in pdf.pages[1:]:
            texto = pagina.extract_text()
            if not texto:
                continue

            patron = re.compile(
                r"([A-Z]+\d+)\s+(\d+)\s+(\d+)\s*[xX]\s*(\d+)\s+([\d.,]+)\s+[\d.,]+"
            )

            for match in patron.finditer(texto):
                tipologia = match.group(1)
                cantidad = int(match.group(2))
                ancho = int(match.group(3))
                alto = int(match.group(4))
                precio_unitario = procesar_precio(match.group(5))
                total_producto = (
                    precio_unitario * cantidad if precio_unitario and cantidad else None
                )
                total_presupuesto += total_producto or 0

                productos.append({
                    "tipologia": tipologia,
                    "cantidad": cantidad,
                    "ancho": ancho,
                    "alto": alto,
                    "precio_unitario": precio_unitario,
                    "total_producto": total_producto,
                })

    return {
        "presupuesto_nro": presupuesto_nro,
        "cliente": cliente,
        "obra": obra,
        "total_presupuesto": total_presupuesto,
        "productos": productos
    }
