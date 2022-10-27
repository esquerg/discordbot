FROM alpine:3.14

WORKDIR /usr/src/app

RUN apk update && apk add bash

ENV TOKEN="MTAyNzIwNzgzNzYwNjIyODA1OA.GwbLHy.JYsTep5LQ7wg8Y4yH0Beg7CxTNONt5HWIslK2k"
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY ffmpeg .

RUN bash




