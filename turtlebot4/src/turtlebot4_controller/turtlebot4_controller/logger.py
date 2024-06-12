import os
import datetime

#flag_rec: bool -> permite guardar o no el mensaje en archivos
#flag_print: bool -> permite imprimir o no el mensaje por consola
def logs(message, flag_rec=0, flag_print=1):
    if flag_rec:
        # Accede la directorio actual
        current_dir = os.getcwd()

        # Crear la dirección del archivo
        log_file_path = os.path.join(current_dir, 'logs.txt')

        # Revisa si el archivo existe
        if not os.path.exists(log_file_path):
            # Crea el archivo en caso no exista
            with open(log_file_path, 'w') as f:
                pass  # Crea un archivo vacío

        current_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Mnesaje con formato
        formatted_log_message = f"[{current_timestamp}] {message}"

        # Añade el mensaje
        with open(log_file_path, 'a') as f:
            f.write(formatted_log_message + '\n')  # Append with a newline character
        
    if flag_print:
        print(message)