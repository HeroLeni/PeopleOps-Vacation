import usuarios
import empleados
import vacaciones
import reportes
import os

def limpiar_pantalla():
    # Limpia la consola según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu_principal():
    # Muestra el menú principal de la aplicación
    print("=" * 50)
    print(" PEOPLEOPS VACATION CONSOLE - RIWI")
    print("=" * 50)
    print("1. Gestión de Empleados")
    print("2. Solicitudes de Vacaciones")
    print("3. Aprobar/Rechazar Solicitudes")
    print("4. Historial de Vacaciones")
    print("5. Generar Reporte CSV")
    print("6. Salir")
    print("=" * 50)

def menu_empleados():
    # Controla el submenú de gestión de empleados
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print(" GESTIÓN DE EMPLEADOS")
        print("=" * 50)
        print("1. Registrar nuevo empleado")
        print("2. Listar todos los empleados")
        print("3. Consultar un empleado")
        print("4. Volver al menú principal")
        print("=" * 50)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            empleados.registrar_empleado()
        elif opcion == "2":
            empleados.listar_empleados()
        elif opcion == "3":
            empleados.consultar_empleado()
        elif opcion == "4":
            break
        else:
            print("Opción inválida")
        input("Presione ENTER para continuar...")

def menu_vacaciones():
    # Controla el submenú de solicitudes de vacaciones
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print(" SOLICITUDES DE VACACIONES")
        print("=" * 50)
        print("1. Registrar nueva solicitud")
        print("2. Ver solicitudes pendientes")
        print("3. Volver al menú principal")
        print("=" * 50)
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            vacaciones.registrar_solicitud()
        elif opcion == "2":
            vacaciones.listar_solicitudes_pendientes()
        elif opcion == "3":
            break
        else:
            print("Opción inválida")
        input("Presione ENTER para continuar...")

def main():
    # Función principal: inicializa archivos, maneja login y menú principal
    limpiar_pantalla()
    usuarios.inicializar_usuarios()
    empleados.inicializar_empleados()
    vacaciones.inicializar_vacaciones()
    print("=" * 50)
    print(" BIENVENIDO A PEOPLEOPS VACATION CONSOLE")
    print("=" * 50)
    if not usuarios.iniciar_sesion():
        print("Acceso denegado. Cerrando aplicación...")
        return
    while True:
        limpiar_pantalla()
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            menu_empleados()
        elif opcion == "2":
            menu_vacaciones()
        elif opcion == "3":
            vacaciones.aprobar_rechazar_solicitudes()
            input("Presione ENTER para continuar...")
        elif opcion == "4":
            vacaciones.mostrar_historial()
            input("Presione ENTER para continuar...")
        elif opcion == "5":
            reportes.generar_reporte_mensual()
            input("Presione ENTER para continuar...")
        elif opcion == "6":
            print("Gracias por usar PeopleOps Vacation Console.")
            break
        else:
            print("Opción inválida")
            input("Presione ENTER para continuar...")

if __name__ == "__main__":
    main()
