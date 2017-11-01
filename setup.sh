# copy the exports and aliases to bash_aliases to preserve environment
# variables in case the user's ssh session is disconnected
cp bash_aliases.sh $HOME/.bash_aliases
source $HOME/.bash_aliases

# initializes the task directory
mkdir $TASK_DIR
tar -xvzf $REPO_DIR/task_dir.tgz -C $TASK_DIR

# move user to the task directory
cd $TASK_DIR
