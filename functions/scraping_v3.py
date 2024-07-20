from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json

def scrape_website(url):

    # Configuração do driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Abre a pagina
    driver.get(url)
    driver.maximize_window()

    # Espere a página carregar
    driver.implicitly_wait(1)  

    # Extrai a informação da div 'content_center' que é a pagina que foi acessada
    content_center = driver.find_element(By.CSS_SELECTOR, "div.content_center p.text_center").text

    # Extrai o cabeçalho da tabela
    headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, "table.tb_dados th")]

    # Faz o scraping dos dados selecionando apenas a tabela principal "tb_dados tbody"
    data = []
    table_rows = driver.find_elements(By.CSS_SELECTOR, "table.tb_dados tbody tr")

    # Faz o loop de todas as linhas da tabela e colunas
    for row in table_rows:
        columns = row.find_elements(By.CSS_SELECTOR, "td")
        if columns:  # Ignorar linhas vazias
            item = {headers[i]: columns[i].text for i in range(len(columns))}
            data.append(item)
            # Exibir dados para debug
            print("Row data:", item)

    # Fecha o navegador
    driver.quit()

    # Define os dados finais a serem armazenados
    final_data = {
        "Content": content_center, #cabeçalho
        "table_data": data #dados da tabela
    }

    return final_data
