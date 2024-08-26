# Geo Mapper API Service

## Get started

## Using with docker container (preferably)
1. Run `docker-compose up -d`
2. Open `http://localhost:8000/docs`


## Using local development mode
### Setup Python Virtual Environment and dependencies for local development
### Option 1:
1. Install virtualenv: `pip install virtualenv`
2. Create new virtual environment.
    * Unix-based: `virtualenv -p python3 venv`
3. Activate created virtualenv.
    * Unix-based: `. venv/bin/activate`
4. In terminal run `pip install pdm`
5. Under project root directory write the next command `pdm install` to install dependencies
### Option 2:
***Be sure you have poetry installed***
1. Install virtualenv: `pdm venv create`
2. Activate created virtualenv `pdm venv activate`
3. Install dependencies: `poetry install`

#### *See more [pdm documentation](https://pdm-project.org/en/latest/)*

### Setup ENV variables according to .env.example file

### Start app
1. Run `python app/main.py` *to run app you need to set up Postgres.app to your machine
2. Open `http://localhost:8080/latest/docs`

## Alembic
1. After having any changes in schema run `alembic revision --autogenerate -m "<commit message>"`
2. To upgrade db run `alembic upgrade head`

## Set up git hook
1. Install pre-commit library `pip install pre-commit`. Could be skipped if all project requirements already satisfied
2. Implement pre-commit for current project `pre-commit install`

## Test running
1. `python -m pytest` - just run this command from root folder. Possible to add some additional flags if needed
