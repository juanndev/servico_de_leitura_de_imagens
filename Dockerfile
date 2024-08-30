# Usa uma imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
