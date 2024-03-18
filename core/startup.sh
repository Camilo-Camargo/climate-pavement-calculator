#!/bin/sh
# TODO: Check if the script is running on docker container or outside.
echo "Installing bash..."
apk add bash

echo "Installing dependiencies"
yarn install

if [ $ENV = "prod" ]; then
  echo "------------ PRODUCTION MODE ------------"
  pip install -r requirements.txt
  uvicorn api:app --host 0.0.0.0
else
  echo "------------ DEVELOPMENT MODE ------------"
  echo "Not implemented yet."
fi
