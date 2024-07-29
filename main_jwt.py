from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
from typing import Optional
from functions.scraping import scrape_website

# Criando uma instância do FastAPI
app = FastAPI()

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
        detail="Não foi possivel validar o token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verifica_token(token, credentials_exception)

# Endpoint para gerar e retornar um token de acesso
@app.get("/token", response_model=Token)
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
}

# Definindo o endpoint protegido
@app.get("/api/{ano}/{tipo}")
@app.get("/api/{ano}/{tipo}/{subtipo}")
@app.get("/api/csv/{ano}/{tipo}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
