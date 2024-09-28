import psycopg2
import serial
import datetime

# Configuración del puerto serial
PUERTO_COM = 'COM4'  # Reemplaza con tu puerto COM correcto
VELOCIDAD = 9600

# Función para conectar al puerto serial
def conectar_serial(puerto, velocidad):
    try:
        ser = serial.Serial(puerto, velocidad)
        print(f"Conectado al puerto {puerto} a {velocidad} baudios.")
        return ser
    except serial.SerialException as e:
        print(f"No se pudo abrir el puerto serial: {e}")
        exit()

# Función para conectar a la base de datos PostgreSQL
def conectar_base_datos():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            user="postgres",  # Reemplaza con tu usuario
            password="789654lol",  # Reemplaza con tu contraseña
            database="prueba"  # Asegúrate de que la base de datos sea correcta
        )
        cursor = conexion.cursor()
        print("Conexión con la base de datos establecida.")
        return conexion, cursor
    except psycopg2.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        exit()

# Función principal
def main():
    ser = conectar_serial(PUERTO_COM, VELOCIDAD)
    conexion, cursor = conectar_base_datos()

    try:
        while True:
            if ser.in_waiting > 0:
                # Leer los datos del puerto serial
                dato = ser.readline().decode('utf-8').strip()

                # Extraer solo la parte numérica del dato
                dato_numerico = ''.join(filter(str.isdigit, dato))

                # Validación de datos
                if not dato_numerico:  # Comprobar si está vacío después de filtrar
                    print(f"Dato no válido recibido: {dato}. Se omitirá la inserción.")
                    continue

                # Obtener fecha y hora actual
                fecha_hora_actual = datetime.datetime.now()
                fecha = fecha_hora_actual.strftime("%Y-%m-%d")
                hora = fecha_hora_actual.strftime("%H:%M:%S")

                print(f"Dato recibido: {dato_numerico}, Fecha: {fecha}, Hora: {hora}")

                # Insertar los datos en la base de datos
                sql = "INSERT INTO datos (distancia, fecha, hora) VALUES (%s, %s, %s)"
                val = (dato_numerico, fecha, hora)

                try:
                    cursor.execute(sql, val)
                    conexion.commit()
                    print(f"Dato {dato_numerico} insertado en la base de datos con Fecha: {fecha} y Hora: {hora}.")
                except psycopg2.Error as insert_err:
                    print(f"Error al insertar datos en la base de datos: {insert_err}")
                    conexion.rollback()  # Revertir en caso de error

    except KeyboardInterrupt:
        print("Proceso interrumpido por el usuario.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Cerrar recursos de forma segura
        if ser.is_open:
            ser.close()
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        print("Conexiones cerradas correctamente.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
