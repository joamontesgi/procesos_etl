import os
import psycopg2
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def conexionBaseDatos():
    conexion = psycopg2.connect(
        dbname = os.getenv('DATABASE'),
        host = os.getenv('HOST_DB'),
        user = os.getenv('USER_DB'),
        password = os.getenv('PASSWORD_DB')
    )
    return conexion

def leerArchivo():
    with open('ventas_estadisticas.txt', 'r') as data:
        valores = data.read()
        return valores

def leerConsultas():
    with open('query.txt', 'r') as file:
        lineas = file.readlines()
        return lineas[0].strip(), lineas[1].strip()

def crearTabla():
    conexion = conexionBaseDatos()
    cursor = conexion.cursor()
    consulta_crear = leerConsultas()[1]
    cursor.execute(consulta_crear)
    conexion.commit()
    cursor.close()
    conexion.close()
    return "La tabla se ha credo"

def insertarDatos():
    datos = leerArchivo().split('\n')
    total_ingresos = float(datos[0].split(':')[1].strip())
    promedio = float(datos[1].split(':')[1].strip())
    transacciones = int(datos[2].split(':')[1].strip())
    consulta_insertar = leerConsultas()[0]
    conexion = conexionBaseDatos()
    cursor = conexion.cursor()
    cursor.execute(consulta_insertar, (total_ingresos, promedio, transacciones))
    conexion.commit()
    cursor.close()
    conexion.close()
    return "Se han insertado los datos"
    
def enviarCorreo():
    # Cabeza del correo
    msg = MIMEMultipart()
    destino = 'joamontesgi@unal.edu.co'
    asunto = 'Prueba de correo'
    origen = os.getenv('USER_EMAIL')
    contrasenia = os.getenv('PASSWORD_EMAIL')
    msg['From'] = origen
    msg['To'] = destino
    msg['Subject'] = asunto
    
    # Cuerpo del correo
    msg.attach(MIMEText(leerArchivo(), 'plain'))
    
    # Establecer una conexión con el servidor (Protocolo -> SMTP)
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Se añade capa de seguridad
    servidor.starttls()
    
    # Se inicia la sesión
    servidor.login(origen, contrasenia)
    
    # Se envía el correo
    envio = servidor.sendmail(origen, destino, msg.as_string())
    
    # Se cierra el servidor
    servidor.quit()
    
    if(envio=={}):
        return "El correo fue enviado"
    else:
        return "El correo no fue enviado"

crearTabla()
print(insertarDatos())
print(enviarCorreo())
print(leerArchivo())
print(enviarCorreo())

