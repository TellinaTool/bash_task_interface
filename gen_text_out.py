import os
import json

task_dir = "tasks"
output_dir = "verify_out"


def dfs_filesystem(node, prefix, collector):
	""" traverse the file system dict to collect all file names
		Args:
			node: the current directory to traverse 
			prefix: the dir name
			collector: a list to collect all file names
	"""
	collector.append(prefix + node["name"])
	if "children" in node:
		for child in node["children"]:
			dfs_filesystem(child, prefix + node["name"] + "/", collector)


for fname in os.listdir(task_dir):

	task_name = fname.split(".")[0]
	
	in_file = os.path.join(task_dir, fname)
	out_file = os.path.join(output_dir, task_name + ".out")

	with open(in_file, "r") as f, open(out_file, "w") as g:

		if fname.split(".")[1] != "json":
			continue

		print(fname)

		task = json.load(f)

		if "goal_filesystem" in task and task["goal_filesystem"]:
			goal_fs = task["goal_filesystem"]
			result = []
			dfs_filesystem(goal_fs, "", result)

		# remove this since all folders start with "website" dir
		result = [e.replace("website", ".").replace("./", "") for e in result]

		for e in sorted(result):
			g.write(e + "\n")
