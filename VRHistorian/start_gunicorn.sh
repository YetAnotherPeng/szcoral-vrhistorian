#!/bin/bash

PROJECT_NAME=VRHistorian

gunicorn -c gunicorn.conf.py $PROJECT_NAME.wsgi 
#gunicorn -c gunicorn.conf.py VRHistorian.wsgi
