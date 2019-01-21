#!/usr/bin/env bash

set -e

cd /tmp/ums

docker-compose build ums

cd -

docker-compose up -d

sleep 10

python3 ./scripts/create_users.py
