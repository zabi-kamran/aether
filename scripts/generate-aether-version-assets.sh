#!/usr/bin/env bash
#
# Copyright (C) 2018 by eHealth Africa : http://www.eHealthAfrica.org
#
# See the NOTICE file distributed with this work for additional information
# regarding copyright ownership.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

set +x

mkdir ./tmp/

set -Eeuo pipefail

APP_VERSION=`cat ./VERSION`
# locally use the branch name
APP_REVISION=`git rev-parse --abbrev-ref HEAD`

echo "----------------------------------------------------------------------"
echo "Release version:  $APP_VERSION"
echo "Release revision: $APP_REVISION"
echo "----------------------------------------------------------------------"

echo $APP_VERSION  > ./tmp/VERSION
echo $APP_REVISION > ./tmp/REVISION
