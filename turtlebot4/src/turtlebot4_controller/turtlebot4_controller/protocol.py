from logger import logs

# caracteres de separación
delimitador = "%"
separadorm = "#"
separadorp = "/"

def decodificar(msg):
    encapsulado = msg.split("%")   # El servidor se asegura de recibir solo 1 paquete
    mensaje = encapsulado[1].split("#")

    id_cliente = mensaje[0]

    if len(mensaje) <= 2:
        fin_mensaje = mensaje[1]
        
        info = ("ID cliente" + "\t=\t" + id_cliente + "\n" + 
                "Mensaje" + "\t\t=\t" + fin_mensaje  + "\n")
        logs("\n" + info)
    else:
        nombre_sistema = mensaje[1]
        tipo_sistema = mensaje[2]
        topico = mensaje[3]

        info = ("ID cliente" + "\t=\t" + id_cliente + "\n" + 
                "Nombre sistema" + "\t=\t" + nombre_sistema + "\n" +
                "Tipo de sistema" + "\t=\t" + tipo_sistema + "\n" + 
                "Tópico" + "\t\t=\t" + topico + "\n")

        if mensaje[4] == "s":
            tipo_mensaje = "Subscriber"
                        
            info = (info + 
                    "Tipo de mensaje" + "\t=\t" + tipo_mensaje + "\n")
            logs("\n" + info)  

        elif mensaje[4] == "p":
            tipo_mensaje = "Publisher"
            parametros = mensaje[5]
            
            info = (info + 
                    "Tipo de mensaje" + "\t=\t" + tipo_mensaje + "\n" +
                    "Parámetros" + "\t=\t" + parametros + "\n")
            logs("\n" + info)
        
        else:
            tipo_mensaje = " "
            logs(info)

    return mensaje

def codificar(msg = '', tipo = '', data = ''):
    if msg != '':
        id_cliente = msg[0]
        nombre_sistema = msg[1]
        tipo_sistema = msg[2]
        topico = msg[3]
        if tipo != '':
            tipo_mensaje = tipo
        else:
            tipo_mensaje = msg[4]
        if tipo_mensaje == 'p':
            if data != '':
                parametros = data
            else:
                parametros = msg[5]

    mensaje_cod = (delimitador + 
                   id_cliente + separadorm + 
                   nombre_sistema + separadorm + 
                   tipo_sistema + separadorm + 
                   topico + separadorm +
                   tipo_mensaje)
    if tipo_mensaje == "s":
        mensaje_cod = (mensaje_cod + delimitador)
    else:
        mensaje_cod = (mensaje_cod + separadorm +
                       parametros + delimitador)
            
    return mensaje_cod
