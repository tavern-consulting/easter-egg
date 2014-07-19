#!/bin/sh
coverage run --source='easter_egg/' manage.py test --verbosity=2; coverage report --show-missing --fail-under=100 --omit="*test*.py" && find easter_egg -name '*.py' | xargs flake8
