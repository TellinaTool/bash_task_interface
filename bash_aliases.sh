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
alias abandon="source abandon-task"

# Installing Bash preexec.
curl https://raw.githubusercontent.com/rcaloras/bash-preexec/master/bash-preexec.sh -o ~/.bash-preexec.sh
source ~/.bash-preexec.sh
preexec() {
    # TODO this needs to be disabled for commands like vi since it hangs
    # Store the last command issued by the user into a file.
    echo $1 > $REPO_DIR/user_output/prev_cmd
}

precmd() {
    # The previous command issued by the user.
    PREV_CMD=`cat $REPO_DIR/user_output/prev_cmd`
    # if the previous command was not a diff command, reset command, or a task command
    if [ "$PREV_CMD" != "diff" ] && [ "$PREV_CMD" != "reset" ] && [ "$PREV_CMD" != "task" ]; then
        TASK_NUM=`cat $CURR_TASK`
        # Verify the output of the previous command.
        $REPO_DIR/scripts/verify_task.py $TASK_NUM $SECONDS $PREV_CMD 
        EXIT=$?
        # if the user passes the task
        if [ "$EXIT" = 1 ]; then
            reset
            echo "-----------------------"
            echo "You have passed task $TASK_NUM!"
            # close the current meld window
            pkill meld
            if [ "$TASK_NUM" = 22 ]; then
                echo "Congratulations! You have finished the study. Go ahead and log out."
            fi
        # else, if the user has gone over time for this task
        elif [ "$EXIT" = 2 ]; then
            abandon
            echo "-----------------------------------"
            echo "You have run out of time on task $TASK_NUM."
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
