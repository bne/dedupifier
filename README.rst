dedupifier
==========

install
::
    virtualenv --python=python3.4 .
    bin/pip install pytest -e .

do
::
    bin/dedupe --help

test
::
    bin/py.test dedupifier
