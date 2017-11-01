# exporting variables
# the directory of the task_interface repo
export REPO_DIR="$HOME/bash_task_interface"
# the actual study directory which is separate from the task_interface repo
export TASK_DIR="$HOME/task"
# file that tracks the current task
export CURR_TASK="$REPO_DIR/task_progress/curr_task"
# prepend task_interface scripts to the user's path
export PATH=$REPO_DIR/bin:$PATH

alias reset="cd $HOME && cd $TASK_DIR"

# Installing Bash preexec.
curl https://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh -o ~/.bash-preexec.sh
source ~/.bash-preexec.sh
preexec() {
    TASK_NUM=`cat $CURR_TASK`
    PREV_COMMAND=$1
    $REPO_DIR/scripts/verify_task_$TASK_NUM.py $PREV_COMMAND
  }

precmd() {
    :
  }
