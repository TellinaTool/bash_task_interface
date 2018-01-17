# TODO: This script must be run from ~/bash_task_interface.
# Issue an error if not; otherwise the tar command below will fail.

# copy the exports and aliases to bash_aliases to preserve environment
# variables in case the user's ssh session is disconnected
cp bash_aliases.sh $HOME/.bash_aliases
source $HOME/.bash_aliases

# initializes the task directory
mkdir $TASK_DIR
tar -xzf $REPO_DIR/task_dir.tgz -C $TASK_DIR

# move user to the task directory
cd $TASK_DIR
