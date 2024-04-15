# Usa una imagen base oficial de Python.
FROM python:3.10.12-slim-buster

# Instala gunicorn para ejecutar la aplicación.
RUN pip install gunicorn

# Copia el archivo de dependencias y las instala.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Copia el directorio de la aplicación.
COPY app/ /app

# Establece el directorio de trabajo.
WORKDIR /app

# Expone el puerto en el que gunicorn ejecutará la aplicación.
EXPOSE 5000

# Define el comando para iniciar la aplicación.
CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "--timeout", "2000", "--access-logfile", "access.log", "--error-logfile", "error.log", "--preload", "wsgi:app"]
