#!/bin/bash

# make a virtual environment and install djiango
pip install --upgrade pip
python3 -m venv myenv
source myenv/bin/activate
pip install django

# run the server on port 8000
python code/manage.py runserver 