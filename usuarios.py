import csv
import os

ARCHIVO_USUARIOS = 'csv/usuarios.csv'

def inicializar_usuarios():
    # Crea el archivo de usuarios con un administrador por defecto si no existe
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['usuario', 'contrasena', 'rol'])
            writer.writeheader()
            writer.writerow({'usuario': 'admin', 'contrasena': 'admin123', 'rol': 'administrador'})
        print(f"Archivo {ARCHIVO_USUARIOS} creado con usuario por defecto")

def validar_credenciales(usuario, contrasena):
    # Valida usuario y contraseña contra el archivo CSV
    try:
        with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['usuario'] == usuario and row['contrasena'] == contrasena:
                    return True, row['rol']
        return False, None
    except FileNotFoundError:
        print(f"Error: El archivo {ARCHIVO_USUARIOS} no existe")
        return False, None

def iniciar_sesion():
    # Maneja el flujo de inicio de sesión con hasta 3 intentos
    intentos = 3
    while intentos > 0:
        print("Inicio de Sesión")
        print(f"Intentos restantes: {intentos}")
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")
        valido, rol = validar_credenciales(usuario, contrasena)
        if valido:
            print(f"Bienvenido, {usuario}. Rol: {rol}")
            return True
        intentos -= 1
        if intentos > 0:
            print("Credenciales incorrectas. Intente nuevamente.")
        else:
            print("Ha excedido el número de intentos permitidos.")
    return False
