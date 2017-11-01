# bash_task_interface

Clone the project to `~/bash_task_interface` on your machine.

Go into the account_setup directory and run `python create_accounts.py` to
create accounts for study participants.

Run `source setup.sh` to setup the system for the study.
This installs bash-preexec (https://github.com/rcaloras/bash-preexec) and sets
up the task directory which will be located at `~/task`.

While in `~/task`, run `task` to see the current task number and task description.

Run `reset` at any time to reset the task directory.
