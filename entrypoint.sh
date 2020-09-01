#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

export PYTHONPATH="/usr/src/tochka-proj/tochka/:$PYTHONPATH"

echo "run migrations"
python ./tochka/manage.py migrate
echo "load test data"
python ./tochka/manage.py loaddata test_accounts.json

exec "$@"
