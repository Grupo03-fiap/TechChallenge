from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
from functions.scraping import scrape_website, scrape_all
import jwt
import csv

# Criando uma instância do FastAPI
app = FastAPI(
    title="API de Scraping da EMBRAPA",
    description="""
Esta API permite acessar dados sobre a produção, processamento, comercialização, importação e exportação de vinhos, sucos e derivados no Brasil.
    
## Introdução
Seja bem-vindo a documentação da API de consulta de dados da Vitivinicultura brasileira!
Nossa API foi criada utilizando o padrão REST que possibilita a integração de seu sistema ao nosso, 
sendo assim você também pode extender ou recriar as funcionalidades existentes na nossa plataforma, 
tudo isso consumindo a API que está documentada abaixo.

## Autenticação

- Para acessar os endpoints protegidos, você precisa obter um token de acesso.
- Use o endpoint `/token` para gerar um token.
- Inclua o token no cabeçalho `Authorization` como um Bearer Token em todas as requisições subsequentes.

## Endpoints Disponíveis

- `/api/{ano}/{tipo}/{subtipo}`: Consulta online de dados por ano e tipo e subtipo.
- `/api/db/update/{anoDe}/{anoAte}`: Atualiza a base de dados offline realizando scraping de todos os anos e tipos especificados.
- `/api/db/consulta/{ano}/{tipo}/{subtipo}`: Consulta os dados armazenados offline por ano e tipo e subtipo.
    """,
    version="v1.0",
    docs_url="/docs"
    
)

# Configuração do JWT
SECRET_KEY = "grupoFIAP03/techChallenge2024"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Função para criar o token JWT usando HS256
def cria_jwt_hash():
    to_encode = {}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar o token JWT
def verifica_token(token: str, credentials_exception):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_exception
    return TokenData(token=token)

# Função de dependência para obter o usuário atual a partir do token
async def valida_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Não foi possível validar o token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verifica_token(token, credentials_exception)

# Endpoint para gerar e retornar um token de acesso
@app.get("/token", response_model=Token, summary="Gerar token de acesso", description="Gera um token JWT para autenticação.")
def gerar_token():
    access_token = cria_jwt_hash()
    return {"access_token": access_token, "token_type": "bearer"}

# Mapear o tipo para o nome da página na URL
tipo_map = {
    'producao': 'opt_02',
    'processamento': 'opt_03',
    'comercializacao': 'opt_04',
    'importacao': 'opt_05',
    'exportacao': 'opt_06',    
}

# Mapear o subtipo para o nome da página na URL
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
    'expsucodeuva': 'subopt_04',
}

# Endpoint de consulta online
@app.get(
    "/api/{ano}/{tipo}",
    summary="Consulta online por ano e tipo",
    description="Consulta os dados diretamente do site por ano e tipo específico, realizando o scraping ao vivo.",
)
@app.get(
    "/api/{ano}/{tipo}/{subtipo}",
    summary="Consulta online por ano, tipo e subtipo",
    description="Consulta os dados diretamente do site por ano, tipo e subtipo específico, realizando o scraping ao vivo.",
)
def get_dados(ano: int, tipo: str, subtipo: str = None, current_user: TokenData = Depends(valida_token)):
    # Construir a URL com ano e tipo
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao={tipo_map[tipo]}"
    
    # Adicionar subtipo à URL, se fornecido
    if subtipo:
        url += f"&subopcao={subtipo_map[subtipo]}"

    # Chamando a função de scraping e passando a URL
    try:
        website_content = scrape_website(url)
        return website_content  # FastAPI converte automaticamente o dicionário Python para JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar scraping: {e}")

# Endpoint de download da base de dados para consulta offline
@app.get(
    "/api/db/update/{anoDe}/{anoAte}",
    summary="Atualizar base de dados offline",
    description="Realiza o scraping de todas as páginas de anos específicos e salva os dados em um arquivo CSV para consulta offline."
)
def get_csv(anoDe: int, anoAte: int, current_user: TokenData = Depends(valida_token)):
    # Chamando a função de scraping e passando a URL
    try:
        scrape_all(anoDe, anoAte)
        return {"status": "success", "message": "Scraping completed successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Endpoint de consulta offline
@app.get(
    "/api/db/consulta/{ano}/{tipo}",
    summary="Consultar base de dados offline por ano e tipo",
    description="Consulta os dados armazenados offline no arquivo CSV com base no ano e tipo.",
)
@app.get(
    "/api/db/consulta/{ano}/{tipo}/{subtipo}",
    summary="Consultar base de dados offline por ano, tipo e subtipo",
    description="Consulta os dados armazenados offline no arquivo CSV com base no ano, tipo e subtipo.",
)
def consulta_offline(ano: int, tipo: str, subtipo: str = None, current_user: TokenData = Depends(valida_token)):
    resultados = []
    
    # Abrir o arquivo CSV e filtrar os dados
    try:
        with open("scraping_data.csv", mode="r", newline="", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row["Year"] == str(ano) and row["Tipo"] == tipo and (subtipo is None or row["Subtipo"] == subtipo):
                    resultados.append(row)
        
        if not resultados:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os parâmetros fornecidos.")
        
        return resultados
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de dados CSV não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o CSV: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
