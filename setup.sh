# copy the exports and aliases to bash_aliases to preserve environment
# variables in case the user's ssh session is disconnected
cp exports-aliases $HOME/.bash_aliases
reset

# create study directory
mkdir $STUDY_DIR 
# initializes the file system for the tasks
r
cd $STUDY_DIR
