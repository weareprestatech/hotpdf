set -e
python -m pipenv run coverage run -m pytest tests/
python -m pipenv run coverage report