#!/bin/bash

virtualenv --python=python3 -q .venv
. .venv/bin/activate
pip install -r requirements.txt
