FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/tochka-proj

RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/tochka-proj/requirements.txt
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps

COPY ./entrypoint.sh /usr/src/tochka-proj/entrypoint.sh

ENTRYPOINT [ "sh", "./entrypoint.sh" ]