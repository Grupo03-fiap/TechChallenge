###API de Web Scraping de Dados de Vitivinicultura da EMBRAPA
Este projeto foi desenvolvido pelo Grupo03 - FIAP como parte do TechChallenge da Pós-Tech em Engenharia de Machine Learning. O objetivo foi criar uma API utilizando FastAPI para realizar operações de web scraping no site da EMBRAPA, focando na extração de dados relacionados à vitivinicultura.

###Instalação
Clonagem do Repositório:
Primeiramente, clonamos o repositório do GitHub para o nosso ambiente local.

###Instalação das Dependências:
Após clonar o repositório, criamos um ambiente virtual e instalamos todas as dependências necessárias para o projeto, conforme listadas no arquivo requirements.txt.

###Configuração do Ambiente:
Asseguramos que o ChromeDriver estivesse corretamente instalado e configurado, já que ele é essencial para o funcionamento do Selenium, uma das ferramentas utilizadas no processo de web scraping.

###Uso
Inicialização da API:
Para iniciar a API, utilizamos o Uvicorn, um servidor ASGI para Python, que nos permitiu rodar o aplicativo FastAPI localmente.

###Endpoints Disponíveis:
Extração de Dados de Vitivinicultura:
Desenvolvemos endpoints para a extração dos dados de vitivinicultura diretamente do site da EMBRAPA, permitindo que os dados fossem acessados e consumidos através de requisições HTTP.

###Testes:
Para testar a API, utilizamos o Postman, que nos permitiu simular requisições HTTP e validar as respostas da API em ambiente local.

###Documentação da API
Preparamos uma documentação interativa da API utilizando o Swagger, acessível através do endereço http://localhost:8000/docs. Isso facilitou a exploração dos endpoints e permitiu uma visualização clara das funcionalidades disponíveis.

###Plano de Deploy
1. Preparação do Ambiente
1.1. Configuração do Servidor
Para o deploy da API, optamos por um servidor VPS, levando em consideração as necessidades de escalabilidade e desempenho. O plano inclui conectar ao servidor via SSH e atualizar o sistema para garantir que todos os pacotes estejam na versão mais recente.

1.2. Instalação de Dependências
Planejamos instalar o Python e o Pip no servidor, seguidos pelo FastAPI e outras bibliotecas necessárias para o funcionamento da aplicação. Também configuraremos o Gunicorn como gerenciador de processos para garantir que a API funcione de maneira eficiente em produção.

2. Desenvolvimento e Configuração da Aplicação
2.1. Configuração do FastAPI
O plano inclui criar o arquivo principal da aplicação FastAPI e configurar o Uvicorn para rodar o aplicativo. Testaremos a aplicação localmente no servidor para assegurar que tudo funcione corretamente antes de prosseguir com as próximas etapas.

3. Configuração do Servidor Web (Nginx)
3.1. Configuração do Nginx
Configuraremos o Nginx para atuar como um proxy reverso, redirecionando o tráfego HTTP para o aplicativo FastAPI rodando no servidor. Essa configuração é fundamental para garantir a segurança e o gerenciamento adequado das requisições.

4. Obtenção de Certificado SSL com Certbot
4.1. Configuração do Certificado
Para garantir a segurança das conexões, utilizaremos o Certbot para adquirir e configurar um certificado SSL para o nosso domínio. O plano inclui configurar a renovação automática do certificado para evitar interrupções futuras.

5. Gerenciamento de Processos
5.1. Executando com Gunicorn
Criaremos um serviço para o Gunicorn no servidor, permitindo que a API seja gerida automaticamente, garantindo sua disponibilidade contínua.

6. Conclusão
Concluiremos o processo de deploy verificando se tudo está funcionando corretamente. Monitoraremos o servidor para garantir que a API esteja rodando sem problemas e que o certificado SSL esteja devidamente configurado.

Contribuição
Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões de melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.
