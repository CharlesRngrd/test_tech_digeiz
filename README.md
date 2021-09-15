# Test Tech Digeiz

## Setup the environnement
pipenv shell
pipenv install

## Run the app
python run.py

## Run tests with coverage
coverage run --omit "*/site-packages/*" -m unittest tests.py && coverage report --show-missing
