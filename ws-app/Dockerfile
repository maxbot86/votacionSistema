# Usa una imagen base oficial de Python
FROM python:3.11

# Copia los archivos de la aplicación al contenedor
COPY ./app/. /app
COPY ./requirements.txt /app

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que usará Flask
EXPOSE 5006

ENV FLASK_APP=app.py
ENV TYPE_ENV=DEV
ENV SENDER_EMAIL=monitoreo@gmail.com.ar
ENV SMTP_SERVER=mail.gmail.com.ar

# Define el comando de inicio
CMD ["flask", "run", "--host=0.0.0.0","--port=5006"]
