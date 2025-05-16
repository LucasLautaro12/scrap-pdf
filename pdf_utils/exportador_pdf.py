from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generar_pdf_comparativo(ruta_salida, productos_anterior, productos_actual, total_anterior, total_actual):
    doc = SimpleDocTemplate(ruta_salida, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elementos = []
    estilos = getSampleStyleSheet()

    elementos.append(Paragraph("📊 Comparativa de Presupuestos", estilos['Title']))
    elementos.append(Spacer(1, 12))

    # Cabecera combinada
    data = [[
        "Tipología", "Cantidad", "Ancho", "Alto", "Precio x U (Ant.)", "Total Ant.",
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
            tip, cant_act, ancho_act, alto_act, f"${pxu_act:,.2f}", f"${total_act:,.2f}",
            f"${variacion:,.2f}"
        ])


    tabla = Table(data, colWidths=[65, 50, 50, 50, 85, 85, 65, 50, 50, 50, 85, 85, 90])

    tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#cccccc")),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 30))

    # 💡 Resumen final
    diferencia = total_actual - total_anterior
    resumen = [
        f"<b>PRESUPUESTO CERRADO:</b> ${total_anterior:,.2f} — SALDO A FAVOR CLIENTE",
        f"<b>PRESUPUESTO MEDIDAS RELEVADAS EN OBRA:</b> ${total_actual:,.2f} — SALDO NUEVOS PRESUPUESTOS",
    ]

    if diferencia > 0:
        resumen.append(f"<b>A PAGAR POR ADICIONALES/CAMBIOS:</b> ${abs(diferencia):,.2f}")
    elif diferencia < 0:
        resumen.append(f"<b>A FAVOR DEL CLIENTE POR CAMBIOS:</b> ${abs(diferencia):,.2f}")
    else:
        resumen.append("<b>SIN CAMBIOS EN MONTO TOTAL</b>")

    for r in resumen:
        elementos.append(Paragraph(r, estilos["Normal"]))
        elementos.append(Spacer(1, 6))

    doc.build(elementos)
