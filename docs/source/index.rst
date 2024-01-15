.. hotpdf documentation master file, created by
   sphinx-quickstart on Sun Jan 14 23:51:19 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

hotpdf
======
.. image:: https://github.com/weareprestatech/hotpdf/actions/workflows/python-app.yml/badge.svg
    :target: https://github.com/weareprestatech/hotpdf/actions/workflows/python-app.yml

This project was started as an internal project @ `Prestatech <http://prestatech.com/>`_ to parse PDF files in a fast and memory efficient way to overcome the difficulties we were having while parsing big PDF files using libraries such as `pdfquery <https://github.com/jcushman/pdfquery>`_.

hotpdf can be used to find and extract text from PDFs.

`Read the docs <#>`_

Pre-requisites
--------------

1. **Ghostscript Installation:**
   hotpdf requires Ghostscript to be installed. Please install it on your system.

   `Download Ghostscript <https://www.ghostscript.com/>`_.

Contributing
------------

1. **Type & Lint Checks:**
   - Use `mypy` to check for types and maintain code quality.
   - Run mypy locally before pushing to prevent lint pipeline failures.
   - hotpdf/ folder should have **strict** mypy type checking
   - Use `flake8` for basic linting.

    .. code-block:: bash

        pipenv run mypy hotpdf/ --check-untyped-defs --strict
        pipenv run mypy tests/ --check-untyped-defs
        pipenv run flake8 hotpdf/ --ignore=E501,W503

2. **Test Coverage:**
   - Check test coverage with the `coverage` library.
   - Aim for 100% test coverage.

    .. code-block:: bash

        pipenv run coverage run --omit="*/test*" -m pytest tests/
        pipenv run coverage report -m --fail-under=100 -m

To view usage please navigate to usage.
Contents
--------

.. toctree::

   usage
   api

License
-------

This project is licensed under the terms of the MIT license.

---
with ❤️ from the team @ `Prestatech GmbH <https://prestatech.com/>`
