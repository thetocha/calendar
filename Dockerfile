FROM python

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./sql /code/sql

#
CMD ["uvicorn", "sql.main:app", "--host", "0.0.0.0", "--port", "80"]