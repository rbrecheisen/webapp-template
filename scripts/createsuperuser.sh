#!/bin/bash
docker-compose exec web bash -c "python manage.py createsuperuser"
