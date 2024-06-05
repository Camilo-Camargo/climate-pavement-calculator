# Climate Pavement Calculator
Climate Pavement Calculator is a tool designed to calculate geotechnical and climatic parameters relevant to pavement design. It utilizes FastAPI for the main API and Remix JS for the web interface.

## Getting started

## Core
To gettting started go to core

```
cd core
```

then, you must install first the requirements using

```
pip install -r requirement.txt
```

and then run the api

```
uvicorn api:app
```

## Web

To getting started go to web

```
cd web
```

then, you must install the depedencies with your favorite dependency manager.

`yarn install`

and then run the remix project

`yarn run dev`


## Production
In production you must copy the build of `web-spa` to static folder in `core`.
