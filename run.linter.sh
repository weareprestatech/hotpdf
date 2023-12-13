set -e
python -m pipenv run mypy hotpdf/ --check-untyped-defs
python -m pipenv run mypy tests/ --check-untyped-defs
python -m pipenv run flake8 hotpdf/ --ignore=E501,W503