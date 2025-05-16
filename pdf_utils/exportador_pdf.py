from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import os

def generar_pdf_comparativo(ruta_salida, datos_anterior, datos_actual):
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=landscape(A4),
        rightMargin=10, leftMargin=10, topMargin=10, bottomMargin=10
    )
    elementos = []
    estilos = getSampleStyleSheet()

    cliente = datos_anterior["cliente"]
    obra = datos_anterior["obra"]
    presupuesto_anterior_nro = datos_anterior["presupuesto_nro"]
    presupuesto_actual_nro = datos_actual["presupuesto_nro"]

    productos_anterior = datos_anterior["productos"]
    productos_actual = datos_actual["productos"]

    total_anterior = datos_anterior["total_presupuesto"]
    total_actual = datos_actual["total_presupuesto"]

    # Encabezado con texto + logo
    texto_izquierda = [
        Paragraph(f"<b>CLIENTE:</b> {cliente}", estilos["Normal"]),
        Paragraph(f"<b>OBRA:</b> {obra}", estilos["Normal"]),
        Paragraph(f"<b>PRESUPUESTO ANTERIOR:</b> {presupuesto_anterior_nro}", estilos["Normal"]),
        Paragraph(f"<b>PRESUPUESTO ACTUAL:</b> {presupuesto_actual_nro}", estilos["Normal"])
    ]

    ruta_logo = os.path.join(os.path.dirname(__file__), "../resources/LogoSinFondo1.png")
    if os.path.exists(ruta_logo):
        logo = Image(ruta_logo, height=40)
    else:
        logo = Paragraph("", estilos["Normal"])

    encabezado_tabla = Table(
        [[texto_izquierda, logo]],
        colWidths=[None, 120]
    )
    encabezado_tabla.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    elementos.append(encabezado_tabla)
    elementos.append(Spacer(1, 8))
    elementos.append(Paragraph("Comparativa de Presupuestos", estilos['Title']))
    elementos.append(Spacer(1, 12))

    # Tabla principal
    data = [[
        f"Presupuesto N° {presupuesto_anterior_nro}", "", "", "", "", "",
        "",
        f"Presupuesto N° {presupuesto_actual_nro}", "", "", "", "", "",
        "Variación"
    ], [
        "Tipología", "Cantidad", "Ancho", "Alto", "Precio x U (Ant.)", "Total Ant.",
        "",
        "Tipología", "Cantidad", "Ancho", "Alto", "Precio x U (Act.)", "Total Act.",
        "Variación"
    ]]

    productos_dict = {p['tipologia']: p for p in productos_anterior}

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
            "",
            tip, cant_act, ancho_act, alto_act, f"${pxu_act:,.2f}", f"${total_act:,.2f}",
            f"${variacion:,.2f}"
        ])

    tabla = Table(data, colWidths=[
        55, 40, 40, 40, 70, 70,
        5,
        55, 40, 40, 40, 70, 70,
        75
    ], repeatRows=2, splitByRow=0)

    tabla.setStyle(TableStyle([
        ('SPAN', (0,0), (5,0)),
        ('SPAN', (7,0), (12,0)),
        ('BACKGROUND', (0,0), (5,0), colors.HexColor("#cce5ff")),
        ('BACKGROUND', (7,0), (12,0), colors.HexColor("#d4edda")),
        ('BACKGROUND', (13,0), (13,0), colors.HexColor("#fff4a3")),

        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 1), 7),
        ('ALIGN', (0, 0), (-1, 1), 'CENTER'),

        ('BACKGROUND', (6, 0), (6, -1), colors.lightgrey),
        ('FONTSIZE', (0, 2), (-1, -1), 8),
        ('ALIGN', (0, 2), (-1, -1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 6))

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
