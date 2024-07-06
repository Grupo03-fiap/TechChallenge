from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrap_website(url: str):
    try:
        options = Options()
        options.add_argument('--headless') #Executa o navegador sem a interface gráfica
        options.add_argument('--no-sandbox') #Desabilita um sandbox que é necessário para alguns ambientes
        options.add_argument('--disable-dev-shm-usage') #Desabilita o uso \dev necessário para alguns ambientes

        # Iniciar o chrome
        driver = webdriver.Chrome(options = options)
        driver.get(url)
        page_content = driver.page_source
        driver.quit()
        
        return page_content
    
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))