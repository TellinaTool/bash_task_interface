def compute_filesystem_diff(container, task, stdout_paths,
                            save_initial_filesystem=False):
    """
    Compute the difference between the current file system on disk and the goal
    file system. Return None if the current file system does not exist.
    Args:
        container: the container object on which the file system is mounted
        task: the task object which contains the definition of the file system
        stdout_paths: the paths detected from the user's terminal standard
            output which shall be annotated on the diff object
        save_initial_filesystem: set to True if the current file system on disk
            should be saved to the Task object
    """
    filesystem_vfs_path = '/{}/home/website'.format(container.filesystem_name)
    current_filesystem = disk_2_dict(pathlib.Path(filesystem_vfs_path),
        json.loads(task.file_attributes))
    if save_initial_filesystem:
        task.initial_filesystem = json.dumps(current_filesystem)
        task.save()

    if current_filesystem is None:
        return None

    goal_filesystem = task.initial_filesystem if task.type == 'stdout' \
        else task.goal_filesystem
    fs_diff = filesystem_diff(current_filesystem, json.loads(goal_filesystem))
    # annotate the fs_diff with the stdout_paths
    annotate_path_selection(fs_diff, task.type, stdout_paths)

    if not contains_error_in_child(fs_diff) and task.task_id == 2:
        files_in_tar = set()
        try:
            tar = tarfile.open(os.path.join(filesystem_vfs_path, 'html.tar'))
            for member in tar.getmembers():
                files_in_tar.add(os.path.basename(member.name))
        except tarfile.ReadError:
            # valid tar file does not exist on the target path
            pass
        if files_in_tar != {'index.html', 'home.html', 'labs.html',
                            'lesson.html', 'menu.html', 'navigation.html'}:
            annotate_node(fs_diff, pathlib.Path('html.tar'),
                          'incorrect')
    return fs_diff

def compute_stdout_diff(stdout, task, current_dir=None, is_ls_command=False):
    """
    Compute the difference between the user's current terminal output and the 
    goal output.
    
    Args:
        stdout: the user's current terminal output
        task: the task object which contains the definition of the file system
        current_dir: the user's current directory
        is_ls_command: the user issued an "ls" command
    Return:
    	e.g.
		[
		    {
			"line": XXX
			"tag": 'correct'
		    },
		    {	
			"line": XXX
			"tag": 'extra'
		    },
		    {
			"line": XXX
			"tag": 'missing'
		    }
		]
    """
    def __equal__(l1, l2, task_id):
        if task_id == 16:
            # loose comparison is enough for tasks that requires date/time
            # to be outputed in a specific format
            path1 = extract_path(l1, current_dir, is_ls_command)
            path2 = extract_path(l2, '~/website', is_ls_command)
            if path1 == path2:
                time_long_iso_re = re.compile(
                    r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}(:\d{2}(\.\d+)?)?')
                if re.search(time_long_iso_re, l1):
                    return True
        elif task_id == 19:
            # loose comparison is enough for tasks that requires the number of
            # lines in a file
            num_of_lines, _ = l2.split()
            num_of_lines_pattern = re.compile(r'{}\s'.format(num_of_lines))
            path1 = extract_path(l1, current_dir, is_ls_command)
            path2 = extract_path(l2, '~/website', is_ls_command)
            if path1 == path2 and (re.search(num_of_lines_pattern, l1)):
                return True
        else:
            return l1 == l2
        return False

    stdout1 = [line.strip() for line in stdout.split('\n') if line]
    stdout2 = [line.strip() for line in task.stdout.split('\n')]

    stdout_diff = []
    tag = 'correct'

    if task.task_id != 10:
        # boolean variable which is used decide if the "total line" should be
        # shown as correct or as an error
        matched_stdout2 = []
        for l1 in stdout1:
            if not l1:
                continue
            matched = False
            for i in range(len(stdout2)):
                if not i in matched_stdout2 and \
                        __equal__(l1, stdout2[i], task.task_id):
                    matched = True
                    matched_stdout2.append(i)
                    break
            if matched:
                line_tag = 'correct'
            else:
                total_pattern = re.compile(r'(total\s|\stotal)')
                current_parent_dir_pattern = re.compile(r'\s(\.|\.\.)$')
                if (re.search(total_pattern, l1) and len(l1) < 20):
                    line_tag = 'correct'
                elif re.search(current_parent_dir_pattern, l1):
                    line_tag = 'correct'
                else:
                    line_tag = 'extra'
            stdout_diff.append({
                'line': l1,
                'tag': line_tag
            })

        for i in range(len(stdout2)):
            if not i in matched_stdout2:
                l2 = stdout2[i]
                stdout_diff.append({
                    'line': l2,
                    'tag': 'missing'
                })
                tag = 'incorrect'
    else:
        i = 0
        j = 0
        while i < len(stdout1) and j < len(stdout2):
            l1 = stdout1[i]
            l2 = stdout2[j]
            path1 = extract_path(l1, current_dir)
            path2 = extract_path(l2, current_dir)

            if path1 and path1 == path2:
                stdout_diff.append({
                    'line': l1,
                    'tag': 'correct'
                })
                i += 1
                j += 1
            else:
                if path1 is None or path1.name < path2.name:
                    stdout_diff.append({
                        'line': l1,
                        'tag': 'extra'
                    })
                    tag = 'incorrect'
                    i += 1
                else:
                    stdout_diff.append({
                        'line': l2,
                        'tag': 'missing'
                    })
                    tag = 'incorrect'
                    j += 1
        if i < len(stdout1):
            for l1 in stdout1[i:]:
                stdout_diff.append({
                    'line': l1,
                    'tag': 'extra'
                })
            tag = 'incorrect'
        if j < len(stdout2):
            for l2 in stdout2[j:]:
                stdout_diff.append({
                    'line': l2,
                    'tag': 'missing'
                })
            tag = 'incorrect'

    return { 'lines': stdout_diff, 'tag': tag }
