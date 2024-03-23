#!/bin/sh
# TODO: Check if the script is running on docker container or outside.
echo "Installing bash..."
apk add bash

echo "Installing dependiencies"
pip install -r requirements.txt

if [ $ENV = "prod" -o $ENV = "prod-build" ]; then
  echo "------------ PRODUCTION MODE ------------"
  uvicorn api:app --host 0.0.0.0
elif [ $ENV = "build" ]; then
  echo "Done."
else
  echo "------------ DEVELOPMENT MODE ------------"
  uvicorn api:app --host 0.0.0.0 --reload
fi
