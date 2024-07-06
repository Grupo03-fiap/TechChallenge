from fastapi import FastAPI
from functions.scraping import scrap_website

app = FastAPI()

@app.get('/api/producao')
def get_producao():
    '''
    Endpoint para acessar os dados de produção
    
    '''
    website_content = scrap_website('http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02')
    return website_content