#!/bin/bash

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="server_postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

#until postgres_ready; do
#  >&2 echo "Postgres is unavailable - sleeping"
#  sleep 1
#done

python manage.py makemigrations app &&
python manage.py migrate &&
gunicorn server.wsgi -w 2 -b 0.0.0.0:8001 -t ${WORKER_TIMEOUT}
