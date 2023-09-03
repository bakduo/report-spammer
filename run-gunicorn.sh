#!/bin/bash

gunicorn authdj.wsgi --log-file -
