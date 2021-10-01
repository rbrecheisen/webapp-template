#!/bin/bash
docker-compose down
git pull
docker-compose up -d db
docker-compose up -d redis
docker-compose up -d rq
docker-compose logs -f
