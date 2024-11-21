# Usa una imagen oficial
FROM python:3.9-buster

# Utilizado para destrabar los logs
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script Python y cualquier otro archivo necesario al contenedor
COPY . /app

# Establecer las variables de entorno necesarias para el correo electrónico
# Es preferible pasarlas cuando se ejecuta el contenedor o en un archivo .env
ENV EMAIL_ADDRESS="pruebascremona@gmail.com"
ENV EMAIL_PASSWORD="dplb esea fqfw aaei"

# Comando para ejecutar el script
CMD ["python", "main.py"]
