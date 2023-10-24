FROM python

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY app /code/app

EXPOSE 8033

#
CMD ["alembic", "revision", "--autogenerate", "-m", "Create a baseline migrations"]
CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8033"]