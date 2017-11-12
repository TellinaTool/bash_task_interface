#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import subprocess
import filecmp

def main():
    task_num = sys.argv[1]
    command = ' '.join(sys.argv[2:])
    print('command: ' + command)
    try:
        output_path = os.environ['REPO_DIR'] + '/user_output/out'
        output_file = open(output_path, 'w')

        devnull = open(os.devnull, 'wb')
        ret = subprocess.call(command, shell=True, stderr=devnull, stdout=output_file)

        # close output file for normalization
        output_file.close()

        norm_out_path = os.environ['REPO_DIR'] + '/user_output/norm_out'

        normalize_output(output_path, norm_out_path)

        if verify(norm_out_path, task_num):
            print('PASSED AYYYY')
            to_next_task(task_num)
        else:
            print('NOPE!!!')
    except subprocess.CalledProcessError:
        pass


def normalize_output(output_path, norm_out_path):
    norm_out = open(norm_out_path, 'w')
    output = open(output_path)
    lines = sorted(output.read().splitlines())
    for line in lines:
        print(line.lstrip('./'), file=norm_out)
    norm_out.close()
    output.close()


def verify(norm_out_path, task_num):
    task_verify_path = os.environ['REPO_DIR'] + '/verify_out/task_' + str(task_num)
    return filecmp.cmp(norm_out_path, task_verify_path)


def to_next_task(task_num):
    curr_task_path = os.environ['REPO_DIR'] + '/task_progress/curr_task'
    with open(curr_task_path, 'w') as curr_task:
        print(int(task_num) + 1, end='', file=curr_task)


if __name__ == '__main__':
    main()
