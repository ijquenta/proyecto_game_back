# Administrador de tokens para los distintos microservicios.

# Servicio de Calculo de Beneficios Sociales

Servicio que calcula el monto de beneficios 

# Ejecucion

### Creacion de entorno virtual

Crear carpeta de entorno virtual de python

`python -m venv .venv`

Por defecto usara la version de python que se tenga instalada, se reconmienda usar las versiones 3.9 a 3.9.12

Para habilitar el entorno

`source .venv/bin/activate`

Nota: es diferente para windows, se recomienda revisar la documentacion

### Instalar dependencias

`pip install -r requirements.txt`

### Levantar App

Levantar de forma nativa

`python app/app.py`

Levantar con gunicorn

`pip install gunicorn`
`cd app`
`gunicorn -w 2 --bind 0.0.0.0:5001 --timeout 1200 --access-logfile aplication.log --error-logfile error.log wsgi:app`