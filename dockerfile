FROM tensorflow/tensorflow:latest-gpu

MAINTAINER Ralph Brecheisen <r.brecheisen@maastrichtuniversity.nl>

COPY src/server /src
COPY requirements.txt /requirements.txt
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN apt-get -y update && \
    apt-get install -y vim libpq-dev && \
    pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    pip install uwsgi gunicorn && \
    mkdir /data && \
    mkdir /data/static && \
    mkdir /data/files

WORKDIR /src

CMD ["/docker-entrypoint.sh"]
