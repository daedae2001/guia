import requests
from bs4 import BeautifulSoup
import csv

def obtener_datos_detalle_programa(url, canal):
    response = requests.get('https://www.tvguia.es' + url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Inicializa las variables con valores predeterminados
        titulo = "Sin datos"
        fecha = "Sin datos"
        hora = "Sin datos"
        descripcion = "Sin datos"
        imagen = "https://imgs.nestimg.com/casa_chalet_en_venta_en_carballo_5070018692436938291.jpg"
        logo = "Sin datos"
        categoria = "Sin datos"
        tipo = "Sin datos"

        titulo_element = soup.find('div', class_='program-title')
        if titulo_element:
            titulo = titulo_element.get_text(strip=True).replace('"', "'")

        logo_element = soup.find('div', class_='program-logo')
        if logo_element:
            logo = logo_element.find('img')['src']

        categoria_element = soup.find('span', class_='program-element program-area-1')
        if categoria_element:
            categoria = categoria_element.get_text(strip=True).replace('"', "'").replace(',', "|")

        fecha_element = soup.find('div', class_="program-date")
        if fecha_element:
            fecha_text = fecha_element.get_text().replace('\xa0', '').replace(",", "").replace('\n', '#').strip('#')
            if (len(fecha_text.split('#')) == 3):
                fecha, hora, tipo = fecha_text.split('#')
            if (len(fecha_text.split('#')) == 2):
                fecha, hora = fecha_text.split('#')
                
            if (len(fecha_text.split('#')) == 1):
                fecha = fecha_text.split('#')
                

        img_div = soup.find('div', style="float:left; margin: 0px 8px 0px 0px;")
        if img_div:
            img_tag = img_div.find('img')
            if img_tag:
                imagen = img_tag.get('src')

        descripcion_element = soup.find('div', class_='program-element')
        if descripcion_element:
            descripcion = descripcion_element.find('p').get_text().replace('"', "'")

        writer.writerow([canal, logo, fecha, hora, titulo, descripcion, tipo, categoria, imagen])

def obtener_datos_adicionales(url, canal):
    response = requests.get('https://www.tvguia.es' + url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        channel_rows = soup.find_all('div', class_='channel-row')

        for channel_row in channel_rows:
            link = channel_row.find('div', class_='channel-programs-row channel-programs-time').find('a')['href']
            obtener_datos_detalle_programa(link, canal)

# Abre el archivo CSV para escritura
with open('tv_program.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['canal', 'logo', 'fecha', 'hora', 'titulo', 'descripcion', 'tipo', 'categoria', 'imagen'])

    url = 'https://www.tvguia.es/tv-manana/programacion-la-1'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        channel_divs = soup.find_all('div', class_='block-channel-programs-div-title')

        for channel_div in channel_divs:
            canal = channel_div.contents[0].get_text()
            href = channel_div.contents[0].attrs['href'].replace('/tv/', '/tv-manana/')
            obtener_datos_adicionales(href, canal)

    else:
        print("Error al realizar la solicitud HTTP")
    url = 'https://www.tvguia.es/tv/programacion-la-1'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        channel_divs = soup.find_all('div', class_='block-channel-programs-div-title')

        for channel_div in channel_divs:
            canal = channel_div.contents[0].get_text()
            href = channel_div.contents[0].attrs['href'].replace('/tv/', '/tv/')
            obtener_datos_adicionales(href, canal)

    else:
        print("Error al realizar la solicitud HTTP")

