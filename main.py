from fastapi import FastAPI
from functions.scraping import scrape_website
from enum import Enum

#Criando uma instância do FastAPI
app = FastAPI()

class consult_aba(str, Enum):
    producao = 'Produção'
    processamento = 'Processamento'
    comercializacao = "Comercialização"
    importacao = "Importação"
    exportacao = "Exportação"

# Mapear o tipo para o nome da pagina na URL
tipo_map = {
    'Produção': 'opt_02',
    'Processamento': 'opt_03',
    'Comercialização': 'opt_04',
    'Importação': 'opt_05',
    'Exportação': 'opt_06',    
}

# Mapear o subtipo para o nome da pagina na URL
subtipo_map = {
    'viniferas': 'subopt_01',
    'vinhodemesa': 'subopt_01',
    'americanas': 'subopt_02',
    'espumantes': 'subopt_02',
    'uvasdemesa': 'subopt_03',
    'uvasfrescas': 'subopt_03',
    'semclassificacao': 'subopt_04',
    'uvaspassas': 'subopt_04',
    'sucodeuva': 'subopt_05',
}

# Definindo o endpoint
@app.get("/api/{ano}/{tipo}")
@app.get("/api/{ano}/{tipo}/{subtipo}")
@app.get("/api/csv/{ano}/{tipo}")

# Função de consulta os campos de pagina , ano e subtipo
def get_dados(tipo: consult_aba,ano: int, subtipo: str = None):
        '''para o campo de subtipo utilizar as seguintes opções
        - viniferas; - vinhodemesa; - americanas; - espumantes; -
         uvasdemesa; - uvasfrescas; - semclassificacao; - uvaspassas; -
         sucodeuva;
        '''
    # Construir a URL com ano e tipo
        url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={tipo_map[tipo]}"
    
    # Adicionar subtipo à URL, se fornecido
        if subtipo:
            url += f"&subopcao={subtipo_map[subtipo]}"

    #Chamando a função de scraping e passando a URL
        try:
            website_content = scrape_website(url)
            return website_content  # FastAPI converte automaticamente o dicionário Python para JSON
        except Exception as e:
            print(f"Erro ao executar scraping: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
