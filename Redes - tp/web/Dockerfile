# Usa Python 3.9 como imagen base (versión ligera)
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "app.py"] 