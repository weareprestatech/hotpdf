=========
hotpdf
=========

This project was started as an internal project @ `Prestatech <http://prestatech.com/>`_ to parse PDF files in a fast and memory efficient way to overcome the difficulties we were having while parsing big PDF files using libraries such as `pdfquery <https://github.com/jcushman/pdfquery>`_.

hotpdf can be used to find and extract text from PDFs.

Installation
------------

The latest version of `hotpdf` can be installed directly from `PYPI`_ with pip.

.. code-block:: bash

   pip install hotpdf

.. _PYPI: https://pypi.org/project/hotpdf/

Local Setup
------------

First install the dependencies required by hotpdf

.. code-block:: bash

   python3 -m pip install -e .


Contributing
------------

You should install the `pre-commit` hooks with ``pre-commit install``. This will run the linter, mypy, and a subset of the tests on every commit.

For more examples of how to run the full test suite, please refer to the `CI workflow <https://github.com/weareprestatech/hotpdf/blob/main/.github/workflows/test.yml>`_.

We strive to keep the test coverage at 100%: if you want your contributions accepted, please write tests for them :D

Some examples of running tests locally:

.. code-block:: bash

   python3 -m pip install -e '.[testing]'               # install extra deps for testing
   python3 -m pytest -n=auto test/                      # run the test suite
   # run tests with coverage
   python3 -m pytest --cov-fail-under=96 -n=auto --cov=hotpdf --cov-report term-missing


Known Issues
--------------

1. (cid:x) characters in text - Some pdfs when extracted, some symbols like `€` might not be properly decoded, and instead be extracted as `(cid:128)`.

   This is a problem with the `pdfminer.six` library. We have fixed it from our side on our `fork <https://github.com/weareprestatech/pdfminer.six>`, and you can install it using pip. Until we are able to merge it to pdfminer.six repo and it gets released, we recommend that you install our fork with the fixes manually.

   .. code-block:: bash
   
      pip install --no-cache-dir git+https://github.com/weareprestatech/pdfminer.six.git@20240222#egg=pdfminer-six



Documentation
--------------

We use `sphinx <https://www.sphinx-doc.org/en/master/>`_ for generating our docs and host them on `readthedocs <https://readthedocs.org/>`_.

Please update and add documentation if required, with your contributions.

Update the `.rst` files, rebuild them, and commit them along with your PRs.

.. code-block:: bash

    cd docs
    make clean
    make html

This will generate the necessary documentation files. Once merged to `main` the docs will be updated automatically.


Contents
--------------

To view detailed usage information, please navigate to `Usage` and `User Guide`


.. toctree::
   :maxdepth: 3
   :caption: Contents:

   usage
   guide
   api

License
-------

This project is licensed under the terms of the MIT license.

---
with ❤️ from the team @ `Prestatech GmbH <https://prestatech.com/>`_
