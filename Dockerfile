FROM alpine:3.14

WORKDIR /usr/src/app

RUN apk update && apk add bash

ENV TOKEN="MTAyNzIwNzgzNzYwNjIyODA1OA.GdeN60.skY6MWeGs-h1jEeeqr32jtxB5V9kONyUXnSndE"
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY bot.py .

RUN bash




