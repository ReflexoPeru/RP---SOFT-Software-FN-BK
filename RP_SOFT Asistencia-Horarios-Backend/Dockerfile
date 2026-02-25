FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema para mysqlclient (necesario para conectar a MySQL)
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando por defecto (se puede sobrescribir en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
