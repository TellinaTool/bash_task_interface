# bash_task_interface

This repository contains code to record user commands and test their correctness.

## Developer setup

Clone the project to `~/bash_task_interface` on your machine, via one of these commands:
```
cd && git clone git@github.com:TellinaTool/bash_task_interface.git
cd && git clone https://github.com/TellinaTool/bash_task_interface.git
```

To create accounts for study participants, from the clone run
```python account_setup/create_accounts.py```

## User setup

In a user account, run `source setup.sh`.
This installs bash-preexec (https://github.com/rcaloras/bash-preexec) and sets
up the task directory which will be located at `~/task`.

## User usage

While in `~/task`:
 * run `task` to see the current task number and task description.
 * run `reset` to reset the task directory.
