# Usa una imagen base de Python
FROM python:3.11-alpine3.19

# Dependencias para psycopg2
RUN apk add build-base libpq libpq-dev

# Copia los archivos de la app
COPY . /code

# Establece el directorio de trabajo
WORKDIR /code

# Instala las dependencias
RUN pip install -r requirements.txt

ENV PYTHONPATH=/code

# Comando para ejecutar la aplicación
CMD ["python", "-u", "main.py"]