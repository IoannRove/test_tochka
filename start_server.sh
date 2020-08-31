#!/bin/sh

mv examples/env .env
docker-compose -f docker-compose.prod.yml up --build