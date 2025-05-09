#!/usr/bin/env python
import re
import sys

MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
PROJECT_SLUG = '{{ cookiecutter.project_slug }}'

if not re.match(MODULE_REGEX, PROJECT_SLUG):
    print(f'ERROR: {PROJECT_SLUG} is not a valid Python module name!')
    sys.exit(1)