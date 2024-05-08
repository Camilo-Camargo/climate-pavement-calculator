#!/bin/sh

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
