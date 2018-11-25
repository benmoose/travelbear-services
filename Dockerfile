FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements*.txt ./
RUN pip install -r requirements.test.txt

COPY . .
