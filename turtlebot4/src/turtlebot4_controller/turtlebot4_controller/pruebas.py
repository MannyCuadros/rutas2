import socket

# Variables globales
host = "192.168.99.2"  # Reemplaza con la IP del host deseado
ports = [22, 80, 443, 1445, 11311, 32854, 32941, 33081, 33171, 
         34963, 35188, 35296, 35465, 35552, 36129, 37174, 37241, 
         37818, 38337, 38709, 38807, 39122, 39937, 39959, 40368, 
         40945, 41531, 42287, 42625, 42665, 43207, 43227, 43314, 
         43626, 44091, 44394, 44587, 45433, 45498, 45537, 45647, 
         45908, 46229, 46717, 46810, 47904, 48151, 48901, 51097, 
         51350, 57282, 58312, 58505, 60216]  # Reemplaza con la lista de puertos deseada


ports2 = [22, 80, 443, 1445, 11311, 32871, 33251, 33794, 34550, 
          34865, 35027, 35439, 36297, 36369, 36681, 36864, 37012, 
          37541, 37636, 37651, 38460, 39103, 39547, 40008, 40025, 
          40220, 40443, 40775, 41427, 41805, 42062, 42257, 42756, 
          42850, 42905, 43215, 43242, 43449, 43765, 44684, 44990, 
          45100, 45150, 45324, 45672, 49996, 51686, 53376, 54010, 
          54374, 54958, 55817, 60702, 60935]

ports3 = [22, 1445, 11311, 32819, 33799, 34026, 34047, 34862, 
          34915, 35571, 35674, 36052, 36403, 37164, 38126, 38208, 
          38215, 38690, 39009, 39023, 39061, 39212, 39585, 39987, 
          40072, 40693, 41422, 41761, 42521, 42642, 42966, 43177, 
          43256, 43545, 43902, 43923, 44669, 44749, 45373, 45689, 
          47406, 48459, 48986, 51296, 52100, 52333, 52704, 53853, 
          56049, 58978, 60873, 60984]


message = "{\"msg_id\":\"ROBOT_BODY_CTRL_CMD\",\"body_part\":2,\"action\":6}"  # Reemplaza con el mensaje deseado
#message = "{\"msg_id\":\"ROBOT_GET_BATTERY_REQ\"}"

def scan_ports():
    print(f"ingresando al host {host}...")
    for port in ports3:
        print(f"Escaneando puerto {port}...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Tiempo de espera de 1 segundo por puerto
        try:
            s.connect((host, port))
            print(f"Conexión exitosa al puerto {port}")
            try:
                s.sendall(message.encode())
                print(f"Mensaje enviado exitosamente al puerto {port}")
                
                s.settimeout(3)  # Tiempo de espera de 3 segundos para la respuesta
                try:
                    response = s.recv(1024)
                    print(f"Respuesta del servidor en el puerto {port}: {response.decode()}")
                except socket.timeout:
                    print(f"No se recibió respuesta del servidor en el puerto {port} dentro del tiempo esperado")
            except Exception as e:
                print(f"Error al enviar el mensaje al puerto {port}: {e}")
            s.close()
        except socket.error:
            print(f"No se pudo establecer conexión al puerto {port}")
        finally:
            s.close()

def puertos_repetidos(lista1, lista2):
    # Convertir ambas listas a conjuntos para eliminar duplicados y permitir operaciones de intersección
    set1 = set(lista1)
    set2 = set(lista2)
    
    # Obtener la intersección de ambos conjuntos
    repetidos = set1.intersection(set2)
    
    # Convertir el conjunto resultante a una lista y devolverla
    return list(repetidos)


if __name__ == "__main__":
    scan_ports()
    #print(message)
    #puertos_comunes = puertos_repetidos(ports, ports2)
    #print(f"Puertos que se repiten en ambas listas: {puertos_comunes}")
