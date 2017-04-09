#!/usr/bin/python
###########################################
# 2017/04/07 Translate d to d.py
# Use "ssh-key adding to authorized file" method to cancel password input(stupid).
# Why not using paramiko or pexpect? Becuase these modules are not installed by default.

import sys
import os
import getpass
#print sys.argv[0]
#import paramiko

def usage():
	print "Usage:", sys.argv[0], "hostname [title1] [title2] [title3]..."
	print "\thostname: Required, if first time executiion, need input and IP, username and passwd."
	print "\ttitle: Optional, you can title your window or using a default one."
	print "\te.g:",sys.argv[0], "atca2"
	print "\te.g:", sys.argv[0], "atca2 subshl spa"

usage()

#if getpass.getuser() == 'root':
#	print "heihei"
os.system('ls -al')
#print os.path.expanduser('~')
#print os.environ['HOME']
#print os.path.expandvars('$HOME')
home  = os.environ['HOME']
rsa_pub = home + '/.ssh/id_rsa.pub'
rsa = home + '/.ssh/id_rsa'
def push_rsa():
	
	if os.path.isfile(rsa_file) and os.path.isfile(rsa):  # if public key exists
		#push id_rsa.pub to remote side	
		print "wakaka"
		
	else:
		# generate id_rsa.pub first, then push to remote.
		print "lalala"
		

def match_user(alias,user,ip):
	labinfo = os.getcwd() + '/lab_info'
	# if find user and IP in lab_info, return them. 
	line = ['\n', alias, user, ip, '\n']
	if os.path.isfile(labinfo):
		print "lab_info file found."
		
	else:
		# if not define lab_info before, define them and return. 
		print "lab_info file not found, new one!"
		f = open(labinfo, 'w')
		f.write('|'.join(line))
		f.close()


def ssh_remote():

	if True:
		pass	
	else:
		pass



if __name__ == "__main__":
	match_user('a', 'root', '192.168.32.170')
