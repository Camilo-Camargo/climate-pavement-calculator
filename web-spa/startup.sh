#!/bin/sh
# TODO: Check if the script is running on docker container or outside.
echo "Installing bash..."
apk add bash

echo "Installing dependiencies"
yarn install

if [ $ENV = "prod" -o $ENV = "prod-build" -o $ENV = "build" ]; then
  echo "------------ PRODUCTION MODE ------------"
  yarn build
  cd build
    rm -rf /core/public
    mv ./client /core/public
  cd ..
else
  echo "------------ DEVELOPMENT MODE ------------"
  yarn run dev
fi
