""" create_accounts.py creates accounts, from files usernames.txt and passwords.txt

This is used to create accounts for the study participants.
"""

import subprocess
import crypt

# get usernames
usernames = open('usernames.txt').read().strip().split('\n')
passwords = open('passwords.txt').read().strip().split('\n')

for username,password in zip(usernames, passwords):
	print "Creating account for", u, "..."

	encrypted_password = crypt.crypt(password,"22") # "22" is the salt
	cmd = "useradd -m -p %s %s" % (password, username)
	print subprocess.check_output(cmd.split())

	## No longer necessary because of use of -p option to useradd
	# # set the passwords
	# cmd = "echo %s:%s" % (username, password)
	# p1 = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	# p2 = subprocess.Popen(["chpasswd"], stdin=p1.stdout)

	# set default shell to bash
	cmd = "usermod -s /bin/bash %s" % username
	print subprocess.check_output(cmd.split())

	# prevent other users from accessing home
	cmd = "chmod 0700 /home/%s" % username
	print subprocess.check_output(cmd.split())
