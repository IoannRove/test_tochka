#!/bin/sh

cp examples/env .env -n
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python tochka/manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec web python tochka/manage.py collectstatic --no-input --clear
