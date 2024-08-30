# Serviço de Medição de Consumo de Água e Gás
## Visão Geral
Este projeto implementa um serviço back-end para o gerenciamento de leituras de consumo de água e gás utilizando Flask, SQLite e Docker. O sistema foi desenvolvido seguindo princípios de Clean Code e está preparado para funcionar em um ambiente de contêiner com Docker, garantindo portabilidade e facilidade de implementação.

### Funcionalidades
Captura de Leituras: Utiliza a API Google Gemini para processar imagens dos medidores e extrair automaticamente as leituras de consumo.
Gerenciamento de Clientes: Interface para registrar e gerenciar clientes e suas respectivas leituras de consumo.
API RESTful: Endpoints para listar, validar e confirmar as leituras dos medidores.
Persistência de Dados: Banco de dados SQLite para armazenar todas as informações relacionadas às leituras e aos clientes.
### Estrutura do Projeto
app/: Contém a lógica principal da aplicação, incluindo os módulos de rotas, modelos e configuração.
docker-compose.yml: Arquivo de configuração do Docker Compose para orquestrar os contêineres da aplicação e do banco de dados.
Dockerfile: Define o ambiente Docker para o serviço web.

## Como Executar
### Clone o Repositório:
git clone https://github.com/juanndev/servico_de_leitura_de_imagens

### Suba os Contêineres com Docker Compose:
docker-compose up --build

## Acessar a Aplicação:

A aplicação estará disponível em: http://127.0.0.1:5000

Uma mensagem de "Bem-vindo ao serviço de medição!" será exibida ao acessar a aplicação com sucesso.

## Observações
Ambiente de Desenvolvimento: O servidor está configurado para desenvolvimento. Para produção, recomenda-se o uso de um servidor WSGI como Gunicorn.
API Google Gemini: A integração com a API está configurada, mas a chave de API deve ser adicionada manualmente no código.
