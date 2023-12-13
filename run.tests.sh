set -e
python -m pipenv run coverage run --omit="*/test*" -m pytest tests/
python -m pipenv run coverage report -m