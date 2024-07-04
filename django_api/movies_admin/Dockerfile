FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install --upgrade pip
RUN pip install -r requirements.txt