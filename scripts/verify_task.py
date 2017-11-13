#!/usr/bin/env python

from __future__ import print_function
import sys
import os
import subprocess
import filecmp
import tarfile

FILESYSTEM_TASKS = {2, 3, 4, 5, 6, 11, 12, 15, 20, 22}

def main():
    task_num = sys.argv[1]
    command = ' '.join(sys.argv[2:])
    try:
        output_path = os.environ['REPO_DIR'] + '/user_output/out'
        output_file = open(output_path, 'w')

        devnull = open(os.devnull, 'wb')
        if int(task_num) in FILESYSTEM_TASKS:
            ret = subprocess.call('find .', shell=True, stderr=devnull, stdout=output_file)
        else:
            ret = subprocess.call(command, shell=True, stderr=devnull, stdout=output_file)

        # close output file for normalization
        output_file.close()

        norm_out_path = os.environ['REPO_DIR'] + '/user_output/norm_out'

        normalize_output(output_path, norm_out_path)

        if verify(norm_out_path, task_num):
            print('PASSED AYYYY')
            to_next_task(task_num)
        else:
            pass
    except subprocess.CalledProcessError:
        pass


def normalize_output(output_path, norm_out_path):
    norm_out = open(norm_out_path, 'w')
    output = open(output_path)
    lines = sorted(output.read().splitlines())
    for line in lines:
        if line == './' or line == '.':
            p_line = line
        else:
            p_line = line.lstrip('./')
        print(p_line, file=norm_out)
    norm_out.close()
    output.close()


def verify(norm_out_path, task_num):
    task_verify_path = os.environ['REPO_DIR'] + '/verify_out/task_' + str(task_num)

    # special verification for task 2
    if task_num == 2:
        files_in_tar = set()
        try:
            tar = tarfile.open(os.path.join(os.environ['TASK_DIR'], 'html.tar'))
            for member in tar.getmembers():
                files_in_tar.add(os.path.basename(member.name))
        except tarfile.ReadError:
            # valid tar file does not exist on the target path
            pass
        if files_in_tar != {'index.html', 'home.html', 'labs.html',
                            'lesson.html', 'menu.html', 'navigation.html'}:
            return False

    # compare normalized output file and task verification file
    return filecmp.cmp(norm_out_path, task_verify_path)


def to_next_task(task_num):
    curr_task_path = os.environ['REPO_DIR'] + '/task_progress/curr_task'
    with open(curr_task_path, 'w') as curr_task:
        print(int(task_num) + 1, end='', file=curr_task)


if __name__ == '__main__':
    main()
