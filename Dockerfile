# Usa una imagen base ligera con Python
FROM python:3.12-slim

# Establece variables de entorno para evitar la escritura de bytecode y para que el output sea inmediato
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Agregar gnupg antes de usar apt-key
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    gnupg \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Agregar el repositorio de Microsoft
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Crea el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el código de la aplicación al contenedor
COPY . /app

# Instala las dependencias de Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expone el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]