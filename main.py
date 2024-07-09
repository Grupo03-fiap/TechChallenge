from fastapi import FastAPI, Query
from functions.scraping import scrap_website

#Criando uma instância do FastAPI
app = FastAPI()

#Definindo um endpoint
@app.get('/api/producao')
def get_producao(ano: int = Query(None, description = 'Ano de produção')):
    '''
    Endpoint para acessar os dados de produção.
    
    Parâmetros:
    - ano: ano de produção que será usado para gerar a URL.
    '''
    #Verificando o parâmetro "ano"
    if ano:
        #Se o ano for passado, monta a URL com o ano especificado
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
    else:
        #Se o ano não for passado, utiliza a URL padrão sem ano
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'

    #Chamando a função de scraping e passando a URL
    website_content = scrap_website(url)

    #Retornando o conteúdo da página
    return website_content