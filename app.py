from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde otros orígenes

@app.route('/')
def index():
    return "Bienvenido a la API de datos."

def conectar_base_datos():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            user="postgres",  # Reemplaza con tu usuario
            password="789654lol",  # Reemplaza con tu contraseña
            database="prueba"  # Asegúrate de que la base de datos sea correcta
        )
        return conexion
    except psycopg2.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

@app.route('/api/datos', methods=['GET'])
def obtener_datos():
    conexion = conectar_base_datos()
    if conexion is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conexion.cursor()
    cursor.execute("SELECT distancia, fecha, hora FROM datos")
    resultados = cursor.fetchall()
    
    # Cerrar la conexión
    cursor.close()
    conexion.close()

    # Convertir los resultados a una lista de diccionarios
    datos = []
    for distancia, fecha, hora in resultados:
        # Convertir hora a cadena
        hora_str = hora.strftime("%H:%M:%S") if isinstance(hora, datetime.time) else hora
        datos.append({'distancia': distancia, 'fecha': fecha, 'hora': hora_str})

    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)
