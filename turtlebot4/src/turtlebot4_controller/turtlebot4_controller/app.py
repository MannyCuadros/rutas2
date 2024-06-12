import json
import os

ruta = "/home/ubuntu20/ros2_ws/src/turtlebot4_controller/turtlebot4_controller/"


def escribir_datos():
    print("Ingrese los datos solicitados\n")
    nombre = input("Nombre completo: ")
    edad = int(input("Edad: "))
    ciudad = input("Ciudad: ")
    aficiones = input("Aficiones separadas por comas: ")
    aficiones_lista = aficiones.split(",")

    datos = {
        "Nombre": nombre,
        "Edad": edad,
        "Ciudad": ciudad,
        "Aficiones": aficiones_lista
    }

    ruta_carpeta = nombre
    ruta_archivo = ruta_carpeta + "/" + nombre + ".json"

    if os.path.exists(ruta_archivo):
        # El archivo existe, actualizamos los datos
        with open(ruta_archivo, "r") as archivo_lectura:
            datos_existentes = json.load(archivo_lectura)

        datos.update(datos_existentes)  # Combinamos los datos nuevos con los existentes

        with open(ruta_archivo, "w") as archivo_escritura:
            json.dump(datos, archivo_escritura, indent=4)

        print(f"Los datos de {nombre} han sido actualizados")
    else:
        # El archivo no existe, creamos los datos
        with open(ruta_archivo, "w") as archivo:
            json.dump(datos, archivo, indent=4)

        print(f"Los datos de {nombre} han sido creados")

def leer_datos():
    nombre = input("Ingrese el nombre de la persona que desea ver:\n")
    ruta_archivo = ruta + nombre + ".json"

    if not os.path.exists(ruta_archivo):
        print(f"{nombre} no se encuentra en la base de datos")
        return

    with open(ruta_archivo, "r") as archivo:
        datos = json.load(archivo)

    print(f"\nNombre: {datos['Nombre']}")
    print(f"Edad: {datos['Edad']}")
    print(f"Ciudad: {datos['Ciudad']}")
    print(f"Aficiones: {', '.join(datos['Aficiones'])}")

def main():
    while True:
        print("\nMenú:")
        print("1. Escribir datos")
        print("2. Leer datos")
        print("0. Salir")

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            escribir_datos()
        elif opcion == "2":
            leer_datos()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
