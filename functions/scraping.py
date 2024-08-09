from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time


def scrape_website(url):

    # Configuração do driver
    service = Service("C:/Py/API2/chromedriver.exe")
    #service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

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
            #print("Row data:", item)

    # Fecha o navegador
    driver.quit()

    # Define os dados finais a serem armazenados
    final_data = {
        "Content": content_center, #cabeçalho
        "table_data": data #dados da tabela
    }

    return final_data

def scrape_all(anoDe, anoAte):
    
    # Dicionario das paginas
    pages_map = {
        'producao': 'opt_02',
        'processamento': 'opt_03',
        'comercializacao': 'opt_04',
        'importacao': 'opt_05',
        'exportacao': 'opt_06',
    }

    subpages_map = {
        'processamento': {
            'viniferas': 'subopt_01',
            'americanas': 'subopt_02',
            'uvasdemesa': 'subopt_03',
            'semclassificacao': 'subopt_04',
        },
        'importacao': {
            'vinhodemesa': 'subopt_01',
            'espumantes': 'subopt_02',
            'uvasfrescas': 'subopt_03',
            'uvaspassas': 'subopt_04',
            'sucodeuva': 'subopt_05',
        },
        'exportacao': {
            'vinhodemesa': 'subopt_01',
            'espumantes': 'subopt_02',
            'uvasfrescas': 'subopt_03',
            'sucodeuva': 'subopt_04',
        },
    }
        
    # Configuração do driver
    service = Service("C:/Py/API2/chromedriver.exe")
    #service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    #options.add_argument('--no-sandbox')
    #options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)

    base_url = "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={tipo}"

    with open("scraping_data.csv", mode="a", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        if file.tell() == 0:
            csv_writer.writerow(["Ano", "Tipo", "Subtipo", "Cabeçalho", "Dados"])

        for year in range(anoDe, anoAte + 1):
            for tipo, tipo_value in pages_map.items():
                if tipo in subpages_map:
                    # Se o tipo tiver subtipos, pule o scraping da página principal
                    for subtipo, subtipo_value in subpages_map[tipo].items():
                        subtipo_url = f"{base_url.format(year=year, tipo=tipo_value)}&subopcao={subtipo_value}"
                        try:
                            driver.get(subtipo_url)
                            driver.implicitly_wait(1)
                            content_center = driver.find_element(By.CSS_SELECTOR, "div.content_center p.text_center").text
                            headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, "table.tb_dados th")]
                            table_rows = driver.find_elements(By.CSS_SELECTOR, "table.tb_dados tbody tr")

                            data = []
                            for row in table_rows:
                                columns = row.find_elements(By.CSS_SELECTOR, "td")
                                if columns:
                                    item = {headers[i]: columns[i].text for i in range(len(columns))}
                                    data.append(item)

                            save_to_csv(csv_writer, year, tipo, subtipo, content_center, data)
                        except Exception as e:
                            print(f"Erro ao fazer scraping do ano {year}, tipo {tipo}, subtipo {subtipo}: {e}")
                else:
                    # Se não houver subtipos, faça o scraping da página principal
                    url = base_url.format(year=year, tipo=tipo_value)
                    try:
                        driver.get(url)
                        driver.implicitly_wait(1)
                        content_center = driver.find_element(By.CSS_SELECTOR, "div.content_center p.text_center").text
                        headers = [header.text for header in driver.find_elements(By.CSS_SELECTOR, "table.tb_dados th")]
                        table_rows = driver.find_elements(By.CSS_SELECTOR, "table.tb_dados tbody tr")

                        data = []
                        for row in table_rows:
                            columns = row.find_elements(By.CSS_SELECTOR, "td")
                            if columns:
                                item = {headers[i]: columns[i].text for i in range(len(columns))}
                                data.append(item)

                        save_to_csv(csv_writer, year, tipo, None, content_center, data)
                    except Exception as e:
                        print(f"Erro ao fazer scraping do ano {year}, tipo {tipo}: {e}")

    driver.quit()
    print("Scraping concluído e dados armazenados em scraping_data.csv.")

def save_to_csv(csv_writer, year, tipo, subtipo, content, data):
    for row in data:
        csv_writer.writerow([year, tipo, subtipo, content, row])
    