import pdfplumber
import re

import re

def procesar_precio(texto_precio):
    if not texto_precio:
        return None
    
    texto = texto_precio.strip()

    # Si tiene tanto coma como punto, determinamos qué es decimal y qué es miles
    # Regla simple: si la coma está después del punto (ej: 1,000,896.94), entonces el punto es decimal
    # Si el punto está antes de la coma (ej: 663.912,36), entonces la coma es decimal

    if ',' in texto and '.' in texto:
        ultima_coma = texto.rfind(',')
        ultima_punto = texto.rfind('.')
        if ultima_punto > ultima_coma:
            # Punto decimal, coma miles
            # Quitar todas las comas, el punto lo dejamos
            texto = texto.replace(',', '')
        else:
            # Coma decimal, punto miles
            texto = texto.replace('.', '').replace(',', '.')
    else:
        # Si solo tiene coma, puede ser decimal o miles (suponemos decimal)
        if texto.count(',') == 1 and texto.count('.') == 0:
            texto = texto.replace(',', '.')
        else:
            # Quitar separadores miles si solo puntos
            texto = texto.replace(',', '').replace('.', '')

    try:
        return float(texto)
    except Exception as e:
        print(f"Error convirtiendo precio '{texto_precio}': {e}")
        return None


def extraer_datos_pdf(ruta_pdf):
    productos = []
    with pdfplumber.open(ruta_pdf) as pdf:
        # Empezamos desde la segunda página (índice 1)
        for pagina in pdf.pages[1:]:
            tablas = pagina.extract_tables()
            for tabla in tablas:
                # Omitimos la fila encabezado (suponemos que es la primera)
                for fila in tabla[1:]:
                    if len(fila) < 5:
                        continue
                    
                    tipologia = fila[0]
                    cantidad = fila[1]
                    medida = fila[2]
                    precio_unitario = fila[3]
                    # total = fila[4]  # Podés usar si querés
                    
                    # Convertir cantidad a int
                    try:
                        cantidad = int(cantidad)
                    except:
                        cantidad = None
                    
                    # Extraer ancho y alto de medida (formato "ancho x alto")
                    ancho = alto = None
                    if medida:
                        match = re.match(r"(\d+)\s*[xX]\s*(\d+)", medida)
                        if match:
                            ancho = int(match.group(1))
                            alto = int(match.group(2))
                    
                    # Convertir precio unitario a float
                    precio_unitario = procesar_precio(precio_unitario)
                    
                    producto = {
                        "tipologia": tipologia,
                        "cantidad": cantidad,
                        "ancho": ancho,
                        "alto": alto,
                        "precio_unitario": precio_unitario,
                    }
                    productos.append(producto)
    
    return productos
