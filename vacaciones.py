import csv
import os
from datetime import datetime, timedelta
import empleados

ARCHIVO_VACACIONES = 'csv/vacaciones.csv'

def inicializar_vacaciones():
    # Crea el archivo de vacaciones si no existe
    if not os.path.exists(ARCHIVO_VACACIONES):
        with open(ARCHIVO_VACACIONES, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['empleado_id', 'nombre_empleado', 'fecha_inicio_vacaciones', 'fecha_fin_vacaciones', 'dias_calculados', 'estado', 'mes', 'anio'])
            writer.writeheader()
        print(f"Archivo {ARCHIVO_VACACIONES} creado")

def calcular_meses_trabajados(fecha_inicio_str):
    # Calcula la cantidad de meses completos trabajados desde la fecha de inicio
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%d/%m/%Y')
    fecha_actual = datetime.now()
    meses = (fecha_actual.year - fecha_inicio.year) * 12
    meses += fecha_actual.month - fecha_inicio.month
    if fecha_actual.day < fecha_inicio.day:
        meses -= 1
    return max(0, meses)

def calcular_dias_sin_domingos(fecha_inicio_str, fecha_fin_str):
    # Calcula la cantidad de días entre dos fechas excluyendo los domingos
    fecha_inicio = datetime.strptime(fecha_inicio_str, '%d/%m/%Y')
    fecha_fin = datetime.strptime(fecha_fin_str, '%d/%m/%Y')
    dias_totales = 0
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        if fecha_actual.weekday() != 6:
            dias_totales += 1
        fecha_actual += timedelta(days=1)
    return dias_totales

def obtener_dias_aprobados(empleado_id):
    # Suma los días de vacaciones aprobados de un empleado
    dias_aprobados = 0
    try:
        with open(ARCHIVO_VACACIONES, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['empleado_id'] == str(empleado_id) and row['estado'] == 'APROBADA':
                    dias_aprobados += int(row['dias_calculados'])
    except FileNotFoundError:
        pass
    return dias_aprobados

def calcular_dias_disponibles(empleado):
    # Calcula los días de vacaciones disponibles y los meses trabajados
    meses_trabajados = calcular_meses_trabajados(empleado['fecha_inicio_contrato'])
    dias_acumulados = meses_trabajados * 1.5
    dias_usados = obtener_dias_aprobados(empleado['empleado_id'])
    return dias_acumulados - dias_usados, meses_trabajados

def registrar_solicitud():
    # Registra una nueva solicitud de vacaciones en estado pendiente
    print("=" * 50)
    print(" REGISTRAR SOLICITUD DE VACACIONES")
    print("=" * 50)
    empleado_id = input("Ingrese el ID del empleado: ")
    empleado = empleados.obtener_empleado_por_id(empleado_id)
    if not empleado:
        print(f"No se encontró un empleado con ID: {empleado_id}")
        return
    dias_disponibles, meses_trabajados = calcular_dias_disponibles(empleado)
    print(f"Empleado: {empleado['nombre_completo']}")
    print(f"Meses trabajados: {meses_trabajados}")
    print(f"Días disponibles: {dias_disponibles:.1f}")
    if meses_trabajados < 6:
        print("El empleado debe tener al menos 6 meses para solicitar vacaciones.")
        print(f"Meses actuales: {meses_trabajados}")
        return
    while True:
        fecha_inicio = input("Fecha de inicio de vacaciones (DD/MM/AAAA): ")
        try:
            datetime.strptime(fecha_inicio, '%d/%m/%Y')
            break
        except ValueError:
            print("Formato de fecha inválido. Use DD/MM/AAAA.")
    while True:
        fecha_fin = input("Fecha de fin de vacaciones (DD/MM/AAAA): ")
        try:
            datetime.strptime(fecha_fin, '%d/%m/%Y')
            break
        except ValueError:
            print("Formato de fecha inválido. Use DD/MM/AAAA.")
    dias_solicitados = calcular_dias_sin_domingos(fecha_inicio, fecha_fin)
    print(f"Días solicitados (sin domingos): {dias_solicitados}")
    if dias_solicitados > dias_disponibles:
        print("No tiene suficientes días disponibles.")
        print(f"Días disponibles: {dias_disponibles:.1f}")
        print(f"Días solicitados: {dias_solicitados}")
        return
    fecha_obj = datetime.strptime(fecha_inicio, '%d/%m/%Y')
    mes = fecha_obj.month
    anio = fecha_obj.year
    with open(ARCHIVO_VACACIONES, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['empleado_id', 'nombre_empleado', 'fecha_inicio_vacaciones', 'fecha_fin_vacaciones', 'dias_calculados', 'estado', 'mes', 'anio'])
        writer.writerow({'empleado_id': empleado_id, 'nombre_empleado': empleado['nombre_completo'], 'fecha_inicio_vacaciones': fecha_inicio, 'fecha_fin_vacaciones': fecha_fin, 'dias_calculados': dias_solicitados, 'estado': 'PENDIENTE', 'mes': mes, 'anio': anio})
    print("Solicitud registrada con estado PENDIENTE.")

def listar_solicitudes_pendientes():
    # Lista en consola todas las solicitudes con estado pendiente
    print("=" * 50)
    print(" SOLICITUDES PENDIENTES")
    print("=" * 50)
    try:
        with open(ARCHIVO_VACACIONES, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            solicitudes = [row for row in reader if row['estado'] == 'PENDIENTE']
            if not solicitudes:
                print("No hay solicitudes pendientes.")
                return
            for i, sol in enumerate(solicitudes, 1):
                print(f"[{i}] Empleado: {sol['nombre_empleado']} (ID: {sol['empleado_id']})")
                print(f"Desde: {sol['fecha_inicio_vacaciones']} - Hasta: {sol['fecha_fin_vacaciones']}")
                print(f"Días: {sol['dias_calculados']} | Estado: {sol['estado']}")
                print("-" * 50)
    except FileNotFoundError:
        print("No se encontró el archivo de vacaciones.")

def aprobar_rechazar_solicitudes():
    # Permite seleccionar una solicitud pendiente y aprobarla o rechazarla
    print("=" * 50)
    print(" APROBAR/RECHAZAR SOLICITUDES")
    print("=" * 50)
    try:
        with open(ARCHIVO_VACACIONES, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            solicitudes = list(reader)
        pendientes = [s for s in solicitudes if s['estado'] == 'PENDIENTE']
        if not pendientes:
            print("No hay solicitudes pendientes.")
            return
        for i, sol in enumerate(pendientes, 1):
            print(f"[{i}] Empleado: {sol['nombre_empleado']} (ID: {sol['empleado_id']})")
            print(f"Desde: {sol['fecha_inicio_vacaciones']} - Hasta: {sol['fecha_fin_vacaciones']}")
            print(f"Días: {sol['dias_calculados']}")
        seleccion = int(input("Seleccione el número de solicitud a procesar: ")) - 1
        if seleccion < 0 or seleccion >= len(pendientes):
            print("Selección inválida.")
            return
        print("1. Aprobar")
        print("2. Rechazar")
        accion = input("Seleccione una acción: ")
        solicitud_objetivo = pendientes[seleccion]
        for s in solicitudes:
            if s == solicitud_objetivo:
                if accion == "1":
                    s['estado'] = 'APROBADA'
                    print("Solicitud aprobada.")
                elif accion == "2":
                    s['estado'] = 'RECHAZADA'
                    print("Solicitud rechazada.")
                else:
                    print("Acción inválida.")
                break
        with open(ARCHIVO_VACACIONES, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['empleado_id', 'nombre_empleado', 'fecha_inicio_vacaciones', 'fecha_fin_vacaciones', 'dias_calculados', 'estado', 'mes', 'anio'])
            writer.writeheader()
            writer.writerows(solicitudes)
    except FileNotFoundError:
        print("No se encontró el archivo de vacaciones.")
    except (ValueError, IndexError):
        print("Entrada inválida.")

def mostrar_historial():
    # Muestra el historial de solicitudes de un empleado
    print("=" * 50)
    print(" HISTORIAL DE VACACIONES")
    print("=" * 50)
    empleado_id = input("Ingrese el ID del empleado: ")
    try:
        with open(ARCHIVO_VACACIONES, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            historial = [row for row in reader if row['empleado_id'] == empleado_id]
            if not historial:
                print(f"No hay historial para el empleado con ID: {empleado_id}")
                return
            print(f"Historial de {historial[0]['nombre_empleado']}:")
            print("=" * 50)
            for sol in historial:
                print(f"Desde: {sol['fecha_inicio_vacaciones']} - Hasta: {sol['fecha_fin_vacaciones']}")
                print(f"Días: {sol['dias_calculados']} | Estado: {sol['estado']}")
                print("-" * 50)
    except FileNotFoundError:
        print("No se encontró el archivo de vacaciones.")
