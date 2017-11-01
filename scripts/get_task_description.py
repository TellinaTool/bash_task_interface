#!/usr/bin/env python

import sys
import json

task_json_filepath = sys.argv[1]

task_json = json.load(open(task_json_filepath))
print(task_json['description'])
