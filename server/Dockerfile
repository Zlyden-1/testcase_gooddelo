FROM python:3.10-slim-buster
RUN apt-get update && apt-get install -y gcc libpq-dev
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN mkdir /app
COPY .env /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY src/ /app/src/
WORKDIR /app/src
