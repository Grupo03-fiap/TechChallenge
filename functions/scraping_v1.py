from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrap_website(url: str):
    '''
    Função para fazer o scraping de uma URL específica.
    Parâmetros:
    - url: URL da página que será feito o scraping
    '''
    try:
        #Configurando o Chrome
        options = Options()
        options.add_argument('--headless') #Executa o navegador sem a interface gráfica
        options.add_argument('--no-sandbox') #Desabilita um sandbox que é necessário para alguns ambientes
        options.add_argument('--disable-dev-shm-usage') #Desabilita o uso \dev necessário para alguns ambientes

        #Iniciando o Chrome
        driver = webdriver.Chrome(options = options)
        #Abrindo URL fornecida
        driver.get(url)
        #Coletando o conteúdo da página
        page_content = driver.page_source
        #Fechando o Chrome
        driver.quit()
        
        #Retornando o conteúdo da página
        return page_content
    
    except Exception as e:
         #Em caso de erro, mostra uma exceção HTTP com código 500 e detalhe do erro
        raise HTTPException(status_code = 500, detail = str(e))