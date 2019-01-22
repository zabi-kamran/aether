#!/usr/bin/env bash

set -e

cd /tmp/ums

docker-compose build ums

cd -

docker-compose up -d
