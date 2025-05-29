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
    tipologia_actual = None
    cantidad_actual = None

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if not texto:
                continue
            lineas = texto.split('\n')

            i = 0
            while i < len(lineas):
                linea = lineas[i].strip()

                # --- FORMATO 1 --- (línea con todo incluido)
                match_f1 = re.match(r'^([A-Z0-9]+)\s+(\d+)\s+(\d+)\s*[xX]\s*(\d+)\s+([\d.,]+)\s+([\d.,]+)', linea)
                if match_f1:
                    tipologia = match_f1.group(1)
                    cantidad = int(match_f1.group(2))
                    ancho = int(match_f1.group(3))
                    alto = int(match_f1.group(4))
                    precio_unitario = procesar_precio(match_f1.group(5))
                    total_producto = procesar_precio(match_f1.group(6))
                    productos.append({
                        "tipologia": tipologia,
                        "cantidad": cantidad,
                        "ancho": ancho,
                        "alto": alto,
                        "precio_unitario": precio_unitario,
                        "total_producto": total_producto,
                    })
                    if total_producto:
                        total_presupuesto += total_producto
                    i += 1
                    continue

                # --- FORMATO 2 --- (encabezado con código largo, seguido por bloques)
                match_encabezado = re.match(r'^([A-Z0-9]+)\s+(\d+)\s+[0-9A-Z]{15,}', linea)
                if match_encabezado:
                    tipologia_actual = match_encabezado.group(1)
                    cantidad_actual = int(match_encabezado.group(2))
                    i += 1
                    continue

                # Si ya hay encabezado activo, buscamos bloques con dimensiones y precios
                if tipologia_actual and cantidad_actual:
                    match_dims = re.search(r'(\d+)\s*[xX]\s*(\d+)', linea)
                    precios = re.findall(r'\$[\s]?[0-9\.,]+', linea)

                    if match_dims and len(precios) >= 2:
                        ancho = int(match_dims.group(1))
                        alto = int(match_dims.group(2))
                        precio_unitario = procesar_precio(precios[0].replace('$', '').strip())
                        total_producto = procesar_precio(precios[1].replace('$', '').strip())
                        productos.append({
                            "tipologia": tipologia_actual,
                            "cantidad": cantidad_actual,
                            "ancho": ancho,
                            "alto": alto,
                            "precio_unitario": precio_unitario,
                            "total_producto": total_producto,
                        })
                        if total_producto:
                            total_presupuesto += total_producto

                i += 1

    return productos
