FROM python:3.12

RUN mkdir /app
WORKDIR /app
COPY ./requirements /app/
RUN pip install -r .\requirements\prod.txt
COPY . /app/
RUN alembic upgrade head

WORKDIR src
CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000