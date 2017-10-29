import subprocess

# get usernames
usernames = open('usernames.txt').read().strip().split('\n')

for u in usernames:
        print "Deleting account for", u, "..."
        cmd = "deluser --remove-home %s" % u
        print subprocess.check_output(cmd.split())
