from fastapi import FastAPI, Query
from functions.scraping import scrape_website

#Criando uma instância do FastAPI
app = FastAPI()

#Definindo um endpoint
@app.get('/api/viti')
def get_informacao(ano: int = Query(None, description = 'Ano da informação'),
                   aba: str = Query(None, description = 'Aba (Produção/Processamento/Comercialização/Importação/Exportação)')):
    '''
    Endpoint para acessar os dados da Vitivinicultura.
    
    Parâmetros:
    - ano: ano que será usado para gerar a URL.
    - aba: aba que será usada para gerar a URL.
    '''
    # Convertendo o texto da aba para o número presente na url
    aba_dict = {
        'Produção': '02',
        'Processamento': '03',
        'Comercialização': '04',
        'Importação': '05',
        'Exportação': '06'
    }

    aba_num = aba_dict.get(aba)

    # Montando a URL com base nos parâmetros fornecidos
    if ano and aba_num:
        #Se o ano e aba forem fornecidos, monta a URL com o ano e a aba especificados
        url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_{aba_num}'
    else:
        #Se o ano e a aba não forem fornecidos, utiliza a URL de apresentação
        url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_01'

    #Chamando a função de scraping e passando a URL
    website_content = scrape_website(url)

    #Retornando o conteúdo da página
    return website_content