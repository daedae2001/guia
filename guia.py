import requests
from bs4 import BeautifulSoup
import csv
import re

# Función para obtener datos adicionales de una URL de detalles
def obtener_datos_adicionales(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Inicializa las variables para almacenar los datos adicionales
        img_src = None
        date_details = None
        title_details = None
        element_details = None
        
        # Busca los elementos dentro de la página
        img = soup.find('img')
        if img:
            img_src = img.get('src')
        
        date_details_element = soup.find('span', class_='date-details')
        if date_details_element:
            date_details = date_details_element.get_text()
        
        title_details_element = soup.find('div', class_='title-details-television')
        if title_details_element:
            title_details = title_details_element.get_text()
        
        element_details_element = soup.find('div', class_='element-details-television')
        if element_details_element:
            element_details = element_details_element.get_text()
        
        # Devuelve los datos adicionales en un diccionario
        datos_adicionales = {
            'img_src': img_src,
            'date_details': date_details,
            'title_details': title_details,
            'element_details': element_details
        }
        
        return datos_adicionales
    else:
        return None

# Realiza la solicitud HTTP para obtener la página web principal
url = 'https://www.tvguia.es/'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    channel_divs = soup.find_all('div', id=re.compile(r'channel-\d+'))
    
    with open('tv_program.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['channel_id', 'alt_logo', 'href_logo', 'div_class', 'tvhour', 'a-details_ch', 'a-details_p', 'a-details_href', 'a-details_text', 'img_src'])

        for channel_div in channel_divs:
            channel_id = channel_div.get('id')
            logo_tag = channel_div.find('a', class_='tvlogo')
            alt_logo = logo_tag.get('alt') if logo_tag else None
            href_logo = logo_tag.get('href') if logo_tag else None
            divs_inside_channel = channel_div.find_all('div')

            for div in divs_inside_channel:
                div_class = div.get('class')[0]
                a_details = div.find('a', class_='a-details')
                if a_details:
                    tvhour_element = div.find('span', class_='tvhour')
                    tvhour = tvhour_element.get_text() if tvhour_element else None
                    a_details_ch = a_details.get('ch')
                    a_details_p = a_details.get('p')
                    a_details_href = 'https://www.tvguia.es' + a_details.get('href')
                    a_details_text = a_details.get_text()

                    img = a_details.find('img')
                    img_src = img.get('data-src') if img else None

                    # Realiza una solicitud adicional para obtener más datos
                    datos_adicionales = obtener_datos_adicionales(a_details_href)
                    img_src = datos_adicionales['img_src']
                    date_details = datos_adicionales['date_details']
                    title_text = datos_adicionales['title_details']
                    element_text = datos_adicionales['element_details']
                    

                    writer.writerow([channel_id, alt_logo, href_logo, div_class, tvhour, a_details_ch, a_details_p, a_details_href, a_details_text, img_src, date_details, title_text, element_text])
                    # Aquí puedes agregar los datos adicionales al archivo CSV si los has obtenido

else:
    print("Error al realizar la solicitud HTTP")
