# exporting variables
# the directory of the task_interface repo
export REPO_DIR="$HOME/bash_task_interface"
# the actual study directory which is separate from the task_interface repo
export TASK_DIR="$HOME/task"
# file that tracks the current task
export CURR_TASK="$REPO_DIR/task_progress/curr_task"
# prepend task_interface scripts to the user's path
export PATH=$REPO_DIR/bin:$PATH
# allows the diff and task number outputs to be turned off
export DIFF_MODE=1

alias reset="cd $HOME && reset && cd $TASK_DIR"
alias toggle="source toggle-diff-mode"


# Installing Bash preexec.
curl https://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh -o ~/.bash-preexec.sh
source ~/.bash-preexec.sh
preexec() {
    # TODO this needs to be disabled for commands like vi since it hangs
    # If we want to see output and the we're not running the diff command, then verify the command.
    echo $1 > $REPO_DIR/user_output/prev_cmd
}

precmd() {
    PREV_CMD=`cat $REPO_DIR/user_output/prev_cmd`
    if [ "$PREV_CMD" != "diff" ] && [ "$PREV_CMD" != "reset" ] && [ "$PREV_CMD" != "task" ]; then
        TASK_NUM=`cat $CURR_TASK`
        $REPO_DIR/scripts/verify_task.py $TASK_NUM $PREV_CMD
        EXIT=$?
        if [ "$EXIT" = 1 ]; then
            reset
            echo "-----------------------"
            echo "You have passed task $TASK_NUM!"
            # close the current meld window
            pkill meld
            if [ "$TASK_NUM" = 22 ]; then
                echo "Congratulations! You have finished the study. Go ahead and log out."
            fi
        fi
    fi
    if [ $DIFF_MODE = 1 ] ; then
        task
    fi
}
