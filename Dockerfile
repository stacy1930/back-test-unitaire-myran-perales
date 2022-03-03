FROM python:3.8.1-slim-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 8000

