import csv

# Define las rutas de entrada y salida
archivo_csv = 'todo.csv'
archivo_m3u = 'todos.m3u'

# Abre el archivo CSV para lectura
with open(archivo_csv, newline='', encoding='latin-1') as csvfile:
    lector_csv = csv.DictReader(csvfile, delimiter=',')
    
    # Abre el archivo M3U para escritura
    with open(archivo_m3u, 'w', encoding='utf-8') as m3ufile:
        # Escribe la cabecera del archivo M3U
        m3ufile.write('#EXTM3U\n')

        # Itera a través de las filas del archivo CSV
        for fila in lector_csv:
            tvg_id =  fila['nombre']
            tvg_name = fila['nombre']
            tvg_logo = fila['tvg-logo']
            group_title = fila['group-title']
            nombre = fila['nombre']
            url = fila['url']

            # Escribe la entrada M3U para cada canal
            m3ufile.write(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" group-title="{group_title}",{nombre}\n')
            m3ufile.write(f'{url}\n')

print(f'Se ha creado el archivo M3U: {archivo_m3u}')
# Define la ruta del archivo M3U de entrada y salida
archivo_m3u_entrada = 'canales.m3u'
archivo_m3u_salida = 'canales_modificado.m3u'

# Abre el archivo M3U de entrada para lectura
with open(archivo_m3u_entrada, 'r', encoding='utf-8') as m3u_entrada:
    lineas = m3u_entrada.readlines()

# Abre el archivo M3U de salida para escritura
with open(archivo_m3u_salida, 'w', encoding='utf-8') as m3u_salida:
    modificar = False  # Esta variable indica si debemos modificar la línea actual

    for linea in lineas:
        if modificar:
            # Reemplaza las entradas tvg-id y tvg-name por el valor de nombre
            linea = linea.replace('tvg-id=""', f'tvg-id="{nombre}"')
            linea = linea.replace('tvg-name=""', f'tvg-name="{nombre}"')
            modificar = False  # Restablece el indicador de modificación

        if '#EXTINF:-1' in linea:
            # Extrae el valor de nombre de la línea #EXTINF
            nombre = linea.split(',', 1)[-1].strip()
            if ' ' in nombre or not nombre:  # Verifica si el nombre está en blanco o contiene espacios
                modificar = True  # Establece el indicador de modificación

        m3u_salida.write(linea)

print(f'Se ha creado el archivo M3U modificado: {archivo_m3u_salida}')

