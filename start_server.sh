#!/bin/sh

cp examples/env .env -n
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate --noinput
docker-compose -f docker-compose.prod.yml exec -T web python manage.py loaddata test_accounts.json
docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --no-input --clear
