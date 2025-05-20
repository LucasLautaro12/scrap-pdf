import pandas as pd

def generar_excel_comparativo(
    ruta_salida, 
    productos_anterior, 
    productos_actual, 
    total_anterior, 
    total_actual,
    cliente=None,
    obra=None,
    ticket=None
):
    # Convertir listas de productos (diccionarios) a DataFrames
    df_anterior = pd.DataFrame(productos_anterior)
    df_actual = pd.DataFrame(productos_actual)

    # Crear un escritor Excel
    with pd.ExcelWriter(ruta_salida, engine='openpyxl') as writer:
        # Escribir hoja presupuesto anterior
        df_anterior.to_excel(writer, sheet_name='Presupuesto Anterior', index=False)

        # Escribir hoja presupuesto actual
        df_actual.to_excel(writer, sheet_name='Presupuesto Actual', index=False)

        # Crear hoja resumen
        resumen = {
            'Cliente': [cliente],
            'Obra': [obra],
            'Ticket Vexar': [ticket],
            'Total Anterior': [total_anterior],
            'Total Actual': [total_actual],
            'Diferencia': [total_actual - total_anterior]
        }
        df_resumen = pd.DataFrame(resumen)
        df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
