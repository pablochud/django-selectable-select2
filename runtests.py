#!/usr/bin/env python

import os
import sys

print(os.environ.get('PWD', "none"))

ret_code = os.system("cd example && ./manage.py validate")

sys.exit(ret_code)
