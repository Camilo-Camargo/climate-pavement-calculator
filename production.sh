#!/bin/sh

PWD=$(pwd)
PRODUCTION_FILE_NAME="production"
PRODUCTION_DIR=$PWD/$PRODUCTION_FILE_NAME
CORE_DIR=$PWD/core
WEB_DIR=$PWD/web-spa
CORE_OUT_DIR=core

mkdir $PRODUCTION_DIR
mkdir $PRODUCTION_DIR/$CORE_OUT_DIR

pushd $WEB_DIR
  yarn install
  ENV=prod yarn run build
  mv build/client $PRODUCTION_DIR/$CORE_OUT_DIR/public
popd

pushd $CORE_DIR
  cp -r * $PRODUCTION_DIR/$CORE_OUT_DIR
popd

cp compose.yml $PRODUCTION_DIR
