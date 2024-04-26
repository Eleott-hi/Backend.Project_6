FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt /app

RUN apt update; apt upgrade -y; 
RUN apt install -y make libpq-dev;
RUN python3 -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt

