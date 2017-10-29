""" create_accounts.py creates all the accounts for the study participants on the machine.
"""

import subprocess

# get usernames
usernames = open('usernames.txt').read().strip().split('\n')
passwords = open('passwords.txt').read().strip().split('\n')

for u,p in zip(usernames, passwords):
	print "Creating account for", u, "..."
	cmd = "useradd -m %s" % u
	print subprocess.check_output(cmd.split())

	# set the passwords
	cmd = "echo %s:%s" % (u, p)
	p1 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	p2 = subprocess.Popen(["chpasswd"], stdin=p1.stdout)

	# set default shell to bash
	cmd = "usermod -s /bin/bash %s" % u
	print subprocess.check_output(cmd.split())

	# prevent other users from accessing home
	cmd = "chmod 0700 /home/%s" % u
	print subprocess.check_output(cmd.split())
