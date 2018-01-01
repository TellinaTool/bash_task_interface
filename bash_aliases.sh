## Variables
# the directory of the task_interface repo
export REPO_DIR="$HOME/bash_task_interface"
# the study directory where the user does work
export TASK_DIR="$HOME/task"
# file that tracks the current task
export CURR_TASK="$REPO_DIR/task_progress/curr_task"
# log file
export LOGFILE="$REPO_DIR/log"
# if nonzero, the shell outputs the diff and task number after each command
export DIFF_MODE=1
# format for timestamps in the bash history
export HISTTIMEFORMAT="%m/%d/%y %T "
# the current treatment condition
export TREATMENT="T"

# prepend task_interface scripts to the user's path
export PATH=$REPO_DIR/bin:$PATH

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
            abandon
            echo "-----------------------"
            echo "You have passed task $TASK_NUM!"
            # close the current meld window
            pkill meld
            if [ "$TASK_NUM" -ge 22 ]; then
                echo "Congratulations! You have finished the study. Go ahead and log out."
            fi
            if [ "$TASK_NUM" = 11 ]; then
                echo "You are halfway through the study!"
                echo "If you were previously using Tellina to complete the tasks, please stop using Tellina for the remaining tasks."
                echo "If you have not been using Tellina to complete the tasks, please open Tellina in your web browser <INSERT LINK>."
            fi
        # else, if the user has gone over time for this task
        elif [ "$EXIT" = 2 ]; then
            abandon
            echo "-----------------------------------"
            echo "You have run out of time on task $TASK_NUM."
            # close the current meld window
            pkill meld
            if [ "$TASK_NUM" -ge 22 ]; then
                echo "Congratulations! You have finished the study. Go ahead and log out."
            fi
            if [ "$TASK_NUM" = 11 ]; then
                echo "You are halfway through the study!"
                echo "If you were previously using Tellina to complete the tasks, please stop using Tellina for the remaining tasks."
                echo "If you have not been using Tellina to complete the tasks, please open Tellina in your web browser <INSERT LINK>."
            fi
        fi
        # if the previous command was an abandon, check the task num
        if [ "$PREV_CMD" = "abandon" ]; then
            pkill meld
            if [ "$TASK_NUM" -ge 22 ]; then
                echo "Congratulations! You have finished the study. Go ahead and log out."
            fi
            if [ "$TASK_NUM" = 11 ]; then
                echo "-----------------------------------"
                echo "You are halfway through the study!"
                echo "If you were previously using Tellina to complete the tasks, please stop using Tellina for the remaining tasks."
                echo "If you have not been using Tellina to complete the tasks, please open Tellina in your web browser <INSERT LINK>."
            fi
        fi
        echo $TASK_NUM,$TREATMENT,$PREV_CMD,$SECONDS,$EXIT >> $LOGFILE
    fi
    if [ $DIFF_MODE = 1 ] ; then
        task
    fi
}

echo "Welcome to the user study!"
echo "At any point, run \"helpme\" to see a list of commands available to you during the study."
echo "For the first half of the study, you will be allowed to use any internet resource to solve the tasks."
echo "Additionally, feel free to use Tellina <INSERT LINK>."
