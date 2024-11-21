# Usa una imagen oficial de Python
FROM python:3.9-slim

# Instalar dependencias necesarias, incluyendo iputils-ping para el comando ping
RUN apt-get update && apt-get install -y iputils-ping

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script Python y cualquier otro archivo necesario al contenedor
COPY . /app

# Instalar las librerías de Python necesarias
RUN pip install smtplib

# Establecer las variables de entorno necesarias para el correo electrónico
# Es preferible pasarlas cuando se ejecuta el contenedor o en un archivo .env
ENV EMAIL_ADDRESS="pruebascremona@gmail.com"
ENV EMAIL_PASSWORD="dplb esea fqfw aaei"

# Comando para ejecutar el script
CMD ["python", "main.py"]