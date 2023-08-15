#!/bin/bash -e

# install dependencies and initialize environment
# use legacy-resolver to work around https://github.com/pypa/pip/issues/9644
python -m pip install -r /rs/project/requirements.txt --require-virtualenv --use-deprecated=legacy-resolver
python -m pip install black isort pip-tools pylint
python -m initenv
