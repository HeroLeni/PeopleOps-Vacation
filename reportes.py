import csv
import empleados as emp
import vacaciones as vac

def generar_reporte_mensual():
    # Genera un archivo CSV con solicitudes aprobadas filtradas por mes y año
    print("=" * 50)
    print(" GENERAR REPORTE MENSUAL")
    print("=" * 50)
    try:
        mes = int(input("Ingrese el mes (1-12): "))
        if mes < 1 or mes > 12:
            print("Mes inválido.")
            return
        anio = int(input("Ingrese el año: "))
        with open(vac.ARCHIVO_VACACIONES, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            solicitudes_filtradas = [row for row in reader if row['mes'] == str(mes) and row['anio'] == str(anio) and row['estado'] == 'APROBADA']
        if not solicitudes_filtradas:
            print(f"No hay solicitudes aprobadas para {mes}/{anio}.")
            return
        nombre_archivo = f"reporte_vacaciones_{anio}_{mes:02d}.csv"
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['empleado_id', 'nombre_empleado', 'cargo', 'area', 'fecha_inicio_vacaciones', 'fecha_fin_vacaciones', 'dias_calculados', 'mes', 'anio']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for sol in solicitudes_filtradas:
                empleado = emp.obtener_empleado_por_id(sol['empleado_id'])
                writer.writerow({'empleado_id': sol['empleado_id'], 'nombre_empleado': sol['nombre_empleado'], 'cargo': empleado['cargo'] if empleado else 'N/A', 'area': empleado['area'] if empleado else 'N/A', 'fecha_inicio_vacaciones': sol['fecha_inicio_vacaciones'], 'fecha_fin_vacaciones': sol['fecha_fin_vacaciones'], 'dias_calculados': sol['dias_calculados'], 'mes': sol['mes'], 'anio': sol['anio']})
        print(f"Reporte generado: {nombre_archivo}")
        print(f"Total de registros: {len(solicitudes_filtradas)}")
    except ValueError:
        print("Entrada inválida. Use números enteros.")
    except FileNotFoundError:
        print("No se encontró el archivo de vacaciones.")
