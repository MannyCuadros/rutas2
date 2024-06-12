import os
import json
from logger import logs

ruta = "/home/ubuntu20/ros2_ws/src/turtlebot4_controller/turtlebot4_controller/"

def saveToFile(datos):
    id_cliente = datos["id_cliente"]
    nombre_sistema = datos["nombre_sistema"]
    tipo_sistema = datos["tipo_sistema"]
    tipo_mensaje = datos["tipo_mensaje"]
    topico = datos["topico"]
    parametros = datos["parametros"]

    ruta_carpeta = ruta + "/" + id_cliente + "/" + nombre_sistema
    ruta_archivo = ruta_carpeta + "/" + topico + ".json"

    if os.path.exists(ruta_archivo):
        # El archivo existe, actualizamos los datos
        with open(ruta_archivo, "r") as archivo_lectura:
            datos_existentes = json.load(archivo_lectura)

        datos.update(datos_existentes)  # Combinamos los datos nuevos con los existentes

        with open(ruta_archivo, "w") as archivo_escritura:
            json.dump(datos, archivo_escritura, indent=4)

        logs(f"\nLos datos de {id_cliente} han sido actualizados\n")
    else:
        # El archivo no existe, creamos los datos
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)

            with open(ruta_archivo, "w") as archivo:
                json.dump(datos, archivo, indent=4)

            logs(f"\nLos datos de {id_cliente} han sido creados\n")