from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm


def generar_pdf_comparativo(ruta_salida, productos_anterior, productos_actual, total_anterior, total_actual):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elementos = []
    estilos = getSampleStyleSheet()

    elementos.append(Paragraph("📊 Comparativa de Presupuestos", estilos['Title']))
    elementos.append(Spacer(1, 12))

    # Cabecera combinada
    data = [[
        "Tipología", "Cantidad", "Ancho", "Alto", "Precio x U (Ant.)", "Total Ant.",
        "",  # Separador visual
        "Tipología", "Cantidad", "Ancho", "Alto", "Precio x U (Act.)", "Total Act.",
        "Variación"
    ]]


    # Mapeamos productos por tipología
    productos_dict = {p['tipologia']: p for p in productos_anterior}

    # Comparamos por tipologías del actual (puede ajustar si querés ordenarlos diferente)
    for actual in productos_actual:
        tip = actual['tipologia']
        anterior = productos_dict.get(tip)

        cant_act = actual['cantidad']
        ancho_act = actual['ancho']
        alto_act = actual['alto']
        pxu_act = actual['precio_unitario']
        total_act = actual['total_producto']

        if anterior:
            cant_ant = anterior['cantidad']
            ancho_ant = anterior['ancho']
            alto_ant = anterior['alto']
            pxu_ant = anterior['precio_unitario']
            total_ant = anterior['total_producto']
        else:
            cant_ant = ancho_ant = alto_ant = pxu_ant = total_ant = 0

        variacion = total_act - total_ant

        data.append([
            tip, cant_ant, ancho_ant, alto_ant, f"${pxu_ant:,.2f}", f"${total_ant:,.2f}",
            "",  # Separador visual
            tip, cant_act, ancho_act, alto_act, f"${pxu_act:,.2f}", f"${total_act:,.2f}",
            f"${variacion:,.2f}"
        ])



    tabla = Table(data, colWidths=[
        60, 45, 45, 45, 80, 80,
        5,   # separador
        60, 45, 45, 45, 80, 80,
        80   # variación
    ])

    tabla.setStyle(TableStyle([
        # Cabecera
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        # Fondos diferenciados
        ('BACKGROUND', (0, 0), (5, 0), colors.HexColor("#d0e1f9")),
        ('BACKGROUND', (7, 0), (12, 0), colors.HexColor("#d2f8d2")),
        ('BACKGROUND', (13, 0), (13, 0), colors.HexColor("#fff4a3")),

        # Columna separadora
        ('BACKGROUND', (6, 0), (6, -1), colors.lightgrey),  # separador visual

        # Texto general
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),

        # Bordes
        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),

        # Espaciado interno
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 30))

    # 💡 Resumen final
    diferencia = total_actual - total_anterior
    resumen_data = [
        ["PRESUPUESTO CERRADO (SALDO A FAVOR CLIENTE):", f"${total_anterior:,.2f}"],
        ["PRESUPUESTO MEDIDAS RELEVADAS EN OBRA (SALDO NUEVOS PRESUPUESTOS):", f"${total_actual:,.2f}"],
    ]

    if diferencia > 0:
        resumen_data.append(["A PAGAR POR ADICIONALES/CAMBIOS:", f"${abs(diferencia):,.2f}"])
    elif diferencia < 0:
        resumen_data.append(["A FAVOR POR ADICIONALES/CAMBIOS:", f"${abs(diferencia):,.2f}"])
    else:
        resumen_data.append(["SIN CAMBIOS EN MONTO TOTAL", ""])

    tabla_resumen = Table(resumen_data, colWidths=[200*mm, 80*mm])
    tabla_resumen.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    elementos.append(Spacer(1, 20))
    elementos.append(tabla_resumen)

    doc.build(elementos)
