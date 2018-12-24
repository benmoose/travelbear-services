FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements*.txt ./
RUN pip install -r requirements.test.txt

COPY . .

EXPOSE 8000
