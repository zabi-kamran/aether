#!/usr/bin/env bash

set -e

cd /tmp

git clone git@github.com:eHealthAfrica/ums.git

cd /tmp/ums

git fetch origin

git checkout feat/rest-api
