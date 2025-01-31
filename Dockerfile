# Use uma imagem base do Python
FROM python:3.11-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos de dependências para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o container
COPY . .

# Exponha a porta que o backend utiliza
EXPOSE 7894

# Comando para iniciar o backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7894", "--reload"]
