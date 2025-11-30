# PeopleOps-Vacation


### Descripción de cada archivo:

- **main.py**: Punto de entrada, maneja el menú principal y coordina todos los módulos
- **usuarios.py**: Gestiona inicio de sesión y validación de credenciales desde CSV
- **empleados.py**: Funciones para registrar, listar y consultar empleados
- **vacaciones.py**: Contiene toda la lógica de cálculo de vacaciones y gestión de solicitudes
- **reportes.py**: Genera reportes CSV filtrados por mes y año

## 🧮 Reglas de Cálculo

### Acumulación de vacaciones
- **1.5 días** por cada mes completo trabajado
- Fórmula: `Días disponibles = (meses completos × 1.5) − días ya aprobados`

### Tiempo mínimo
- Se requieren **6 meses completos** trabajados para solicitar vacaciones

### Cálculo de días solicitados
- Se cuentan todos los días entre fecha inicio y fin
- **Los domingos NO se cuentan** como días de vacaciones
- La validación se realiza automáticamente [web:6][web:9]

## 🎯 Ejemplo de Uso

1. Iniciar sesión con admin/admin123
2. Registrar un empleado con fecha de contrato 01/01/2025
3. Intentar solicitar vacaciones (sistema valida 6 meses mínimos)
4. Después de 6 meses, solicitar vacaciones por 5 días
5. Aprobar la solicitud desde el menú correspondiente
6. Generar reporte mensual en CSV

## ⚠️ Limitaciones y Mejoras Futuras

### Limitaciones actuales:
- Solo un usuario administrador (no hay registro de nuevos usuarios)
- No hay respaldo automático de datos
- Interfaz únicamente en consola
- Sin validación de fechas retroactivas

### Mejoras propuestas:
- 🔄 Agregar roles múltiples (empleado, supervisor, admin)
- 📊 Implementar dashboard con estadísticas
- 🔔 Sistema de notificaciones por email
- 🌐 Migrar a interfaz web con Django
- 🔐 Encriptación de contraseñas
- 📅 Validación de días festivos colombianos
- 💾 Base de datos SQL en lugar de CSV

## 📄 Licencia

Proyecto académico para RIWI - 2025
