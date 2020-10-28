#!/bin/bash

rm mydb.sqlite
python src/load_cities.py
python src/load_test_events.py
python src/run.py
