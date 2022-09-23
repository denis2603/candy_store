FROM python:3
MAINTAINER Zheltikov Denis <den.ari@yandex.ru>

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD bash start.sh
