#!/bin/bash
docker-compose down
git pull
docker-compose up -d && docker-compose logs -f
