#!/usr/bin/env python

import sys
import os
import subprocess

task_num = sys.argv[1]
command = sys.argv[2]

try:
    devnull = open(os.devnull, 'wb')
    output = subprocess.check_output(command.split(), shell=True, stderr=devnull)
    print('from python:')
    print(output)
except subprocess.CalledProcessError:
    pass