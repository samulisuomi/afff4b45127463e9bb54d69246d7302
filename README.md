# afff4b45127463e9bb54d69246d7302

## Prerequisites

- Install Docker and Docker Compose: https://docs.docker.com/compose/install/

## How to run

#### `docker-compose up`

## How to develop

### Prerequisites

- Install Docker and Docker Compose: https://docs.docker.com/compose/install/
- macOS or similar Unix-like OS (not tested on Windows)
- Install Python 3
- Install [Poetry](https://python-poetry.org/)
- Install dependencies with `poetry install`
- To avoid port collision with the backend running in Docker, either:
  - a) Comment out the backend container definition from `docker-compose.yml` so that they don't both collide trying to use 5123. Then run `docker-compose up` again to only start Redis.
  - b) Change the port in the backend run command and the frontend environment variable (see the "Commands" section).

### Commands

#### `poetry run flask run -p 5123`

Starts the development server at http://127.0.0.1:5123

If you change the port, also change the port in `REACT_APP_BACKEND_ROOT_URL` to match and restart the frontend build.

#### `poetry run flask --debug run -p 5123`

Starts the development server in debug mode at http://127.0.0.1:5123 with automatic reloads when code changes happen.

#### `poetry run pytest -v`

Runs the test suite.
