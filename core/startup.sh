#!/bin/sh
# TODO: Check if the script is running on docker container or outside.
echo "Installing bash..."
apk add bash

echo "Installing dependiencies"
pip install -r requirements.txt

if [ $ENV = "prod" ]; then
  echo "------------ PRODUCTION MODE ------------"
  uvicorn api:app --host 0.0.0.0
else
  echo "------------ DEVELOPMENT MODE ------------"
  uvicorn api:app --host 0.0.0.0 --reload
fi
