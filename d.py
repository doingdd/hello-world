#!/usr/bin/python
###########################################
# 2017/04/07 Translate d to d.py
# Use "ssh-key adding to authorized file" method to cancel password input(stupid).
# Why not using paramiko or pexpect? Becuase these modules are not installed by default.

import sys
import os
import getpass
print sys.argv
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

def scp_key(flag, user, ip):
	if flag == 1:
		os.environ['user'] = user
		os.environ['ip'] = ip
		#re_value  = os.system("echo $user $ip ..")
		pool_value = os.system("scp -o StrictHostKeyChecking=no -q \
			   $user@$ip:~/.ssh/authorized_keys ~/.ssh/id_rsa.pub.bk 2> /dev/null")
		## Find ssh-key on remote side. 
		## Check if match with local id_rsa.pub, continue.
		## Check if not match with local then modify and push back
		if pool_value = 0: 
			print "ssh-key pool competed."
			#if key_match:
	
			#else:
					
		## ssh-key not found, need push local to remote, consider remote don't have .ssh
		else: 				
			print "ssh-key not found, push it!"
			os.system("mkdir -p ~/.ssh_temp/.ssh")
			os.system("chmod 700 ~/.ssh_temp/.ssh")
			os.system("cp ~/.ssh/id_rsa.pub ~/.ssh_temp/.ssh/authorized_keys")
			push_value = os.system("scp -o StrictHostKeyChecking=no -r -q \
				     ~/.ssh_temp/.ssh $user@$ip:~/	
			if push_value = 0:
				print "ssh-key push completed!"
			else:
				print "ssh-key push failed!"
			os.system("rm -r ~/.ssh_temp)
			
def push_rsa(user, ip):
	
	if os.path.isfile(rsa_pub) and os.path.isfile(rsa):  # if public key exists
		#push id_rsa.pub to remote side	
		print "wakaka"
		scp_key(1,user,ip)
		
	else:
		# generate id_rsa.pub first, then push to remote.
		os.system('ssh-keygen -t rsa')
		print "ssh-key generate completed on your local"
		
		scp_key(1, user, ip)	

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
			print isplit
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


def ssh_remote():

	if True:
		pass	
	else:
		pass


def main():
	if len(sys.argv) < 2:
		usage()
	user, ip = match_user(sys.argv[1])
	push_rsa(user, ip)
	print user, ip

if __name__ == "__main__":
	main()
