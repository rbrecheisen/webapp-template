#!/bin/bash
docker-compose down
git pull
docker-compose up -d db redis rq && docker-compose logs -f
