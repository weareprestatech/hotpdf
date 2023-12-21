set -e
python -m pipenv run coverage run --omit="*/test*" -m pytest tests/
python -m pipenv run coverage report --fail-under=100 -m