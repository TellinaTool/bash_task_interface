import os
import json

task_dir = "tasks"
output_dir = "verify_out/fs_status"


def dfs_filesystem(node, prefix, collector, selected_only=False):
	""" traverse the file system dict to collect all file names
		Args:
			node: the current directory to traverse 
			prefix: the dir name
			collector: a list to collect all file names
	"""
	if not selected_only:
		collector.append(prefix + node["name"])
	else:
		if "tag" in node and "to_select" in node["tag"] and node["tag"]["to_select"] == 1:
			collector.append(prefix + node["name"])

	if "children" in node:
		for child in node["children"]:
			dfs_filesystem(child, prefix + node["name"] + "/", collector, selected_only)


for fname in os.listdir(task_dir):

	task_name = fname.split(".")[0]
	
	in_file = os.path.join(task_dir, fname)
	out_file = os.path.join(output_dir, task_name + ".fs.out")

	with open(in_file, "r") as f, open(out_file, "w") as g:

		if fname.split(".")[1] != "json":
			continue

		print(fname)

		task = json.load(f)
		
		result = []
		if "goal_filesystem" in task and task["goal_filesystem"]:
			goal_fs = task["goal_filesystem"]
			dfs_filesystem(goal_fs, "", result, False)

		# remove this since all folders start with "website" dir
		result = [e.replace("website", ".").replace("./", "") for e in result]

		for e in sorted(result):
			g.write(e + "\n")
