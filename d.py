#!/usr/bin/python
###########################################
# 2017/04/07 Translate d to d.py
# Use "ssh-key adding to authorized file" method to cancel password input(stupid).
# Why not using paramiko or pexpect? Becuase these modules are not installed by default.

import sys
import os
import getpass
#import paramiko

def usage():
	print "Usage:", sys.argv[0], "hostname [title1] [title2] [title3]..."
	print "\thostname: Required, if first time executiion, need input and IP, username and passwd."
	print "\ttitle: Optional, you can title your window or using a default one."
	print "\te.g:",sys.argv[0], "atca2"
	print "\te.g:", sys.argv[0], "atca2 subshl spa"
	sys.exit()


#if getpass.getuser() == 'root':
#	print "heihei"
#os.system('ls -al')
#print os.path.expanduser('~')
#print os.environ['HOME']
#print os.path.expandvars('$HOME')
home  = os.environ['HOME']
rsa_pub = home + '/.ssh/id_rsa.pub'
rsa = home + '/.ssh/id_rsa'

def scp_key(user, ip):
### this function is a sub function of push_rsa
		os.environ['user'] = user
		os.environ['ip'] = ip
		#re_value  = os.system("echo $user $ip ..")
		pool_value = os.system("scp -o StrictHostKeyChecking=no -q \
			   $user@$ip:~/.ssh/authorized_keys ~/.ssh/id_rsa.pub.bk 2> /dev/null")

		## Find ssh-key on remote side. 
		## Check if match with local id_rsa.pub, continue.
		## Check if not match with local then modify and push back
		if pool_value == 0: 
			print "ssh-key pool competed."
			rsa_pub_bk = home + '/.ssh/id_rsa.pub.bk'
			d = open(rsa_pub_bk)
			pub_key_all = d.read()
			d.close()
			f = open(rsa_pub)
			pub_key_me = f.read()		
			f.close()

			#if key_match:
			if pub_key_me in pub_key_all:
				print "ssh-key matched with remote, no passwd need any more."
				
			else:
				k = open(rsa_pub_bk, 'a+')
				k.write(pub_key_me)
				k.close()
				push_value = os.system("scp -o StrictHostKeyChecking=no -q \
				 ~/.ssh/id_rsa.pub.bk $user@$ip:~/.ssh/authorized_keys")
				if push_value == 0:
					print "ssh-key push completed."
				else:
					print "ssh-key push failed."
					sys.exit()
				
					
		## ssh-key not found, need push local to remote, consider remote don't have .ssh
		else: 				
			print "ssh-key not found on remote, push it!"
			os.system("mkdir -p ~/.ssh_temp/.ssh")
			os.system("chmod 700 ~/.ssh_temp/.ssh")
			os.system("cp ~/.ssh/id_rsa.pub ~/.ssh_temp/.ssh/authorized_keys")
			push_value = os.system("scp -o StrictHostKeyChecking=no -r -q \
				     ~/.ssh_temp/.ssh $user@$ip:~/")
			if push_value == 0:
				print "ssh-key push completed!"
			else:
				print "ssh-key push failed!"
				sys.exit()
			os.system("rm -r ~/.ssh_temp")
			
def push_rsa(user, ip):
	
	if os.path.isfile(rsa_pub) and os.path.isfile(rsa):  # if public key exists
		#push id_rsa.pub to remote side	
		print "ssh-key found in local."	
		scp_key(user,ip)
		
	else:
		# generate id_rsa.pub first, then push to remote.
		print "ssh-key not found in local, need generate it, just press enter from now!"
		os.system('ssh-keygen -t rsa')
		
		scp_key(user, ip)	

def match_user(alias):
	labinfo = os.getcwd() + '/lab_info'
	#line = [ alias, user, ip, '\n']
	user = None
	ip = None
	
	## if find user and IP in lab_info, return them. 
	if os.path.isfile(labinfo):
		print "lab_info file found."
		f = open(labinfo, 'a+')
		for i in f.readlines():
			isplit = i.split('|')
			if alias in isplit:
				f.close()
				user = i.split('|')[1]
				ip = i.split('|')[2]
				return user, ip

		while not user or not ip:
			print "No IP defined before, you need define them: "
			user = raw_input("Please input the username of lab: ")
			ip = raw_input("Please input the IP of lab: ")
		line =  [alias, user, ip, '\n']
		f.write('|'.join(line))
		f.close()
		return user, ip
		
	else:
		# if not define lab_info before, define them and return. 
		print "lab_info file not found, new one!"

		while not user or not ip:
                        print "No IP defined before, you need define them: "
                        user = raw_input("Please input the username of lab: ")
                        ip = raw_input("Please input the IP of lab: ")

                line =  [alias, user, ip, '\n']
		f = open(labinfo, 'w')
		f.write('|'.join(line))
		f.close()
		return user, ip


def ssh_remote(*args):
	print args[3]
	if not args[3]:

		for i in args[3]:
			os.environ['title'] = i
			os.system("dtterm -n $title -e ssh -q -o \
				   StrictHostKeyChecking=no -l $user $ip &")
	
	else:
		os.environ['title'] = args[0]
		os.system("dtterm -n $title -e ssh -q -o \
                           StrictHostKeyChecking=no -l $user $ip &")	

def main():
	if len(sys.argv) < 2:
		usage()
	
	user, ip = match_user(sys.argv[1])
	push_rsa(user, ip)
	ssh_remote(sys.argv[0], user, ip ,sys.argv[1:])

if __name__ == "__main__":
	main()
