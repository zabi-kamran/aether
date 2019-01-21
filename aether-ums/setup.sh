#!/bin/bash

set -Eeuo pipefail

echo "Attempting to create database \"$DB_NAME\""

if psql -c "" $DB_NAME; then
    echo "Database \"$DB_NAME\" exists"
else
    createdb -e $DB_NAME -e ENCODING=UTF8
    echo "Database \"$DB_NAME\" was created"
fi
