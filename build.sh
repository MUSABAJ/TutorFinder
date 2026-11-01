#!/bin/bash
set -e

uv pip install --system -r requirements.txt
python3 manage.py collectstatic --no-input