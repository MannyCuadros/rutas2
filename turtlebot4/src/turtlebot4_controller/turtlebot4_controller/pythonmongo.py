from pymongo import MongoClient
from logger import logs

DBip = "localhost"
DBport = 27017

def connect_to_database():
    client = MongoClient(DBip, DBport)
    logs("Conectado a base de datos en " + DBip + ":" + str(DBport))
    logs("Base de datos actuales: " + str(client.list_database_names()))
    db = client['rutas']
    logs("Conectado a la base de datos \"rutas\"\n")
    return db

def create_or_update_collection(db, nombre_sistema, tipo_sistema, nombre_topico, parametros):
    collection = db[nombre_sistema]

    # Verificar si la colección ya existe
    if nombre_sistema not in db.list_collection_names():
        db.create_collection(nombre_sistema)
    
    # Verificar si el documento ya existe en la colección
    existing_doc = collection.find_one({"Nombre_tópico": nombre_topico})
    if existing_doc:
        # Actualizar el documento existente
        collection.update_one(
            {"_id": existing_doc["_id"]},
            {"$set": {"Parámetros": parametros}})
        logs(f"Los datos de {nombre_sistema} han sido actualizados en la base de datos\n")
    else:
        # Crear un nuevo documento
        collection.insert_one({
            "_id": collection.count_documents({}) + 1,
            "Tipo_sistema": tipo_sistema,
            "Nombre_tópico": nombre_topico,
            "Parámetros": parametros})
        logs(f"Los datos de {nombre_sistema} han sido creados en la base de datos\n")

    # Imprimir las colecciones ordenadas
    print_collections(db)

def print_collections(db):
    logs("Colecciones:")

    for collection_name in sorted(db.list_collection_names()):
            logs(f" - {collection_name}:")
            collection = db[collection_name]
            for document in collection.find():
                logs(f"   {document}")

def search_data(db, nombre_sistema, nombre_topico):
    logs("Buscando datos...")
    collections = db.list_collection_names()
    if nombre_sistema in collections:
        collection = db[nombre_sistema]
        document = collection.find_one({"Nombre_tópico": nombre_topico})
        if document:
            logs("Parámetros" + "\t=\t" + document['Parámetros'])
            '''
            print("Resultado de la búsqueda:")
            print(f"Nombre_sistema: {nombre_sistema}")
            print(f"Tipo_sistema: {document['Tipo_sistema']}")
            print(f"Nombre_tópico: {document['Nombre_tópico']}")
            print(f"Parámetros: {document['Parámetros']}")
            '''
            return document['Parámetros']
        else:
            logs(f"No se encontraron resultados para el tópico ({nombre_topico}) especificado.")
            return "error_topico"
    else:
        logs(f"No se encontraron resultados para el sistema ({nombre_sistema}) especificado.")
        return "error_sistema"
    
'''

def main():
    db = connect_to_database()
    print_collections(db)

    while True:
      print("\n--- Menú ---")
      print("1. Escribir datos")
      print("2. Buscar datos")
      print("3. Salir")
      opcion = input("Seleccione una opción: ")

      if opcion == '1':
        nombre_sistema = input("Ingrese el nombre del sistema: ")
        tipo_sistema = input("Ingrese el tipo de sistema: ")
        nombre_topico = input("Ingrese el nombre del tópico: ")
        parametros = [float(x) for x in input("Ingrese los parámetros separados por '/': ").split('/')]

        create_or_update_collection(db, nombre_sistema, tipo_sistema, nombre_topico, parametros)

      elif opcion == '2':
        nombre_sistema = input("Ingrese el nombre del sistema: ")
        nombre_topico = input("Ingrese el nombre del tópico: ")
        search_data(db, nombre_sistema, nombre_topico)

      elif opcion == '3':
        break

      else:
        print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()

'''