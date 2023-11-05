import re
import csv

# Nombre del archivo M3U de entrada y CSV de salida
archivo_m3u = 'todo.m3u'
archivo_csv = 'todo.csv'

# Expresión regular para analizar las líneas del archivo M3U
m3u_entry_pattern = re.compile(r'#EXTINF:-1 (.*)\n(.*)')

# Crear un archivo CSV y escribir la fila de encabezado
with open(archivo_csv, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';')
    csvwriter.writerow(['tvg-id', 'tvg-name', 'tvg-logo', 'group-title', 'nombre', 'url'])

# Leer el archivo M3U y extraer campos
with open(archivo_m3u, 'r', encoding='utf-8') as m3ufile:
    for line in m3ufile:
        line = line.strip().replace('\n', '')
        # Dividir la línea por la coma
        parts = line.split(',')

        # Obtener la primera parte (texto)
        texto = parts[0].strip()

        # Obtener la segunda parte (nombre)
        if texto.startswith('#EXTINF'):
            nombre = parts[1].replace('\n', '')
            if texto:
                #url = entry_match.group(2)

                # Extraer campos del nombre usando expresiones regulares
                #tvg_id_match = re.search(r'tvg-id="([^"]*)"', texto)
                #tvg_name_match = re.search(r'tvg-name="([^"]*)"', texto)
                tvg_logo_match = re.search(r'tvg-logo="([^"]*)"', texto)
                group_title_match = re.search(r'group-title="([^"]*)"', texto)

                # Asignar valores o cadenas vacías si no se encuentran los campos
                tvg_id =  nombre
                tvg_name = nombre
                tvg_logo = tvg_logo_match.group(1) if tvg_logo_match else ''
                group_title = group_title_match.group(1) if group_title_match else 'sin grupo'
        else:
            url = line
            # Escribir la información en el archivo CSV
            with open(archivo_csv, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=';')
                csvwriter.writerow([tvg_id, tvg_name, tvg_logo, group_title, nombre, url])