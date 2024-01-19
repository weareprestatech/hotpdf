.. hotpdf documentation master file, created by
   sphinx-quickstart on Sun Jan 14 23:51:19 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

hotpdf
======

This project was started as an internal project @ `Prestatech <http://prestatech.com/>`_ to parse PDF files in a fast and memory efficient way to overcome the difficulties we were having while parsing big PDF files using libraries such as `pdfquery <https://github.com/jcushman/pdfquery>`_.

hotpdf can be used to find and extract text from PDFs.

Installation
------------

The latest version of `hotpdf` can be installed directly from `PYPI`_ with pip.

.. code-block:: bash

   pip install hotpdf

.. _PYPI: https://pypi.org/project/hotpdf/


Pre-requisites
--------------

1. **Ghostscript:**
   hotpdf requires Ghostscript to be installed. Please install it on your system.

   `Download Ghostscript <https://www.ghostscript.com/>`_.

Contributing
------------

You should install the `pre-commit` hooks with ``pre-commit install``. This will run the linter, mypy, and a subset of the tests on every commit.

For more examples of how to run the full test suite, please refer to the `CI workflow <https://github.com/weareprestatech/hotpdf/blob/main/.github/workflows/test.yml>`_.

We strive to keep the test coverage at 100%: if you want your contributions accepted, please write tests for them :D

Some examples of running tests locally:

.. code-block:: bash

   python3 -m pip install -e '.[testing]'               # install extra deps for testing
   python3 -m pytest -n=auto test/                      # run the test suite

Contents
--------------

To view detailed usage information, please navigate to `Usage` and `User Guide`


.. toctree::

   usage
   guide
   api

License
-------

This project is licensed under the terms of the MIT license.

---
with ❤️ from the team @ `Prestatech GmbH <https://prestatech.com/>`_
