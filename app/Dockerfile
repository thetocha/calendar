FROM python

WORKDIR /code

COPY ../requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
#COPY .. .

COPY .. /code

EXPOSE 8033

#
CMD ["alembic", "revision", "--autogenerate", "-m", "Docker migration"]
CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8033"]