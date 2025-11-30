import csv
import os
from datetime import datetime

ARCHIVO_EMPLEADOS = 'csv/empleados.csv'

def inicializar_empleados():
    # Crea el archivo de empleados si no existe
    if not os.path.exists(ARCHIVO_EMPLEADOS):
        with open(ARCHIVO_EMPLEADOS, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['empleado_id', 'nombre_completo', 'cargo', 'area', 'fecha_inicio_contrato'])
            writer.writeheader()
        print(f"Archivo {ARCHIVO_EMPLEADOS} creado")

def generar_id_empleado():
    # Genera un nuevo ID entero incremental para un empleado
    try:
        with open(ARCHIVO_EMPLEADOS, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            ids = [int(row['empleado_id']) for row in reader if row['empleado_id']]
            return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1

def registrar_empleado():
    # Registra un nuevo empleado en el archivo CSV
    print("=" * 50)
    print(" REGISTRAR NUEVO EMPLEADO")
    print("=" * 50)
    empleado_id = generar_id_empleado()
    nombre_completo = input("Nombre completo: ")
    cargo = input("Cargo: ")
    area = input("Área: ")
    while True:
        fecha_inicio = input("Fecha de inicio de contrato (DD/MM/AAAA): ")
        try:
            datetime.strptime(fecha_inicio, '%d/%m/%Y')
            break
        except ValueError:
            print("Formato de fecha inválido. Use DD/MM/AAAA.")
    with open(ARCHIVO_EMPLEADOS, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['empleado_id', 'nombre_completo', 'cargo', 'area', 'fecha_inicio_contrato'])
        writer.writerow({'empleado_id': empleado_id, 'nombre_completo': nombre_completo, 'cargo': cargo, 'area': area, 'fecha_inicio_contrato': fecha_inicio})
    print(f"Empleado registrado con ID: {empleado_id}")

def listar_empleados():
    # Muestra en consola todos los empleados registrados
    print("=" * 50)
    print(" LISTA DE EMPLEADOS")
    print("=" * 50)
    try:
        with open(ARCHIVO_EMPLEADOS, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            empleados = list(reader)
            if not empleados:
                print("No hay empleados registrados.")
                return
            for emp in empleados:
                print(f"ID: {emp['empleado_id']}")
                print(f"Nombre: {emp['nombre_completo']}")
                print(f"Cargo: {emp['cargo']}")
                print(f"Área: {emp['area']}")
                print(f"Fecha de inicio: {emp['fecha_inicio_contrato']}")
                print("-" * 50)
    except FileNotFoundError:
        print("No se encontró el archivo de empleados.")

def consultar_empleado():
    # Consulta y muestra la información de un empleado por ID
    print("=" * 50)
    print(" CONSULTAR EMPLEADO")
    print("=" * 50)
    empleado_id = input("Ingrese el ID del empleado: ")
    try:
        with open(ARCHIVO_EMPLEADOS, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for emp in reader:
                if emp['empleado_id'] == empleado_id:
                    print("=" * 50)
                    print(f"ID: {emp['empleado_id']}")
                    print(f"Nombre: {emp['nombre_completo']}")
                    print(f"Cargo: {emp['cargo']}")
                    print(f"Área: {emp['area']}")
                    print(f"Fecha de inicio: {emp['fecha_inicio_contrato']}")
                    print("=" * 50)
                    return emp
            print(f"No se encontró un empleado con ID: {empleado_id}")
            return None
    except FileNotFoundError:
        print("No se encontró el archivo de empleados.")
        return None

def obtener_empleado_por_id(empleado_id):
    # Devuelve un diccionario con los datos del empleado según su ID
    try:
        with open(ARCHIVO_EMPLEADOS, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for emp in reader:
                if emp['empleado_id'] == str(empleado_id):
                    return emp
        return None
    except FileNotFoundError:
        return None
