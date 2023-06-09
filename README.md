API
===

Source code for https://api.dimonalovesanimals.org

## Requirements:

* Python 3.11.4

create a `.env` file:

```
MAILCHIMP_API_KEY=...
```

## Usage:

```commandline
docker-compose up -d
```

It will be auto exposed by [traefik](https://traefik.io/)

## Development

Running in python 3.11.4:

```commandline
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
uvicorn main:app --reload
```

or you can create a `docker-compose.override.yml` file:

```commandline
version: '3.2'

services:
  api:
    command: [ "--port", "80", "--host", "0.0.0.0", "--reload" ]
    volumes:
      - "./main.py:/usr/src/app/main.py"
    ports:
      - "8000:80"
```

and run `docker-compose up --build` with auto reload

then, visit: http://localhost:8000

```
> {"Hello":"World"}
```

Swagger docs will be available
at: http://localhost:8000/docs
or: http://localhost:8000/redoc
