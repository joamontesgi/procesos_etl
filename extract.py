from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import schedule
import time

def extract_data():
    driver = webdriver.Chrome()
    driver.get('https://www.worldometers.info/es/poblacion-mundial/')  # URL del sitio web a extraer
    elements = driver.find_elements(By.ID, 'maincounter-wrap')
    data = {}
    for element in elements:
        key = element.find_element(By.TAG_NAME, 'h1').text
        key = key.replace('ó', 'o')
        value = element.find_element(By.TAG_NAME, 'span').text
        data[key] = value
        
    # Cerrar el navegador
    driver.quit()
    
    # Escribir los datos en un archivo de texto (modo de adición)
    with open('datos_poblacion.txt', 'a') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
    return "Datos extraídos y guardados correctamente"

# Programar la tarea para que se ejecute cada 10 segundos
schedule.every(10).seconds.do(extract_data)

# Ejecutar el programa

while True:
    schedule.run_pending()
    time.sleep(1)
    

