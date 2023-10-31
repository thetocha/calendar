FROM python

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY /app /code/app
COPY /alembic /code/alembic
COPY .env /code/.env
COPY alembic.ini /code/alembic.ini
COPY config.py /code/config.py

EXPOSE 8033
