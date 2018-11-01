#====================================================================
#
#
# Least Update date 			: '18.11.01
# Author 						: Choi Hong Jun
# FACEBOOK 						: https:#www.facebook.com/msjuck
#
#
#====================================================================
#	This is a script for what devices are sending flow packets to a server that this script running on.
#	HOW IT WORKS? : Find out what kind of interfaces server has and dump from each interfaces and then ,finally Analyize dump files.
#	UPDATE LOG  
#
#

import os, re
from multiprocessing import Process

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colored_log(msg, color):
	print color + msg + bcolors.ENDC

def tcpdump(interface, count):
	if 'en' in interface:
		#print "\t[TCPDUMP " + str(os.getpid()) + "] Start dump, " + interface
		#run tcpdump -i eth1 port 2055 -w tcpdump1.pcap	
		cmd = "tcpdump -i " + interface + " -w " + interface + ".pcap -c " + str(count)
		print "\t[TCPDUMP " + str(os.getpid()) + "] " + cmd
		os.popen(cmd)
		#print "\t[TCPDUMP " + str(os.getpid()) + "] End dump, " + interface

def main_loop():
	active_interface = {}
	all_interfaces = os.listdir("/sys/class/net/")

	# 1. Extract Interface and IP
	colored_log("\n\n=== [Stage1] Extract Interface and IP ===\n\n", bcolors.HEADER)
	for interface in all_interfaces:
		try:
			if "en" in interface:
				ipv4 = re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), os.popen('ip addr show ' + interface).read()).groups()[0]
				active_interface[interface] = ipv4 
		except:
			pass
	colored_log("\t<Interface List>", bcolors.OKBLUE)
	for interface in list(active_interface):
		print '\t[%s]:%s' %( interface, active_interface[interface] )

	# 2. TCPDUMP Each Interfaces with Multi-Processing
	colored_log("\n\n=== [Stage2] TCPDUMP Each Interfaces with Multi-Processing ===\n\n", bcolors.HEADER)

	process_list = []
	for interface in list(active_interface):
		colored_log('\t[Create TCPDUMP Process]: ' + interface, bcolors.OKBLUE)
		p = Process(target=tcpdump, args=(interface,100,))
		p.start()
		process_list.append(p)

	#All child processes die here
	for proc in process_list:
		proc.join()		
		print "\t<TCP Dump Process Status>"
		for p in process_list:
			print "\t\t[PID%s] : interface <%s:%s> Status : %s" % (p.pid, p._args[0], active_interface[p._args[0]], "running" if p.is_alive() else "finished")


	# 3. analyze dump files
	colored_log("\n\n=== [Stage3] analyze dump files ===\n\n", bcolors.HEADER)

	src_ip_txt = open('src_ip.txt','w')
	for interface in list(active_interface):
		#cmd = "tshark -r %s -T fields  -e ip.src > %s" %(interface+".pcap", interface+".txt")
		cmd = "tshark -r %s -Y 'udp.port == 2055 || udp.port == 2056' -T fields -e ip.src > %s" %(interface+".pcap", interface+".txt")
		os.popen(cmd)
		src_list = open(interface+".txt").readlines()
		concentrated = "[%s] %s\n" % (interface, "".join(set(src_list)))
		src_ip_txt.write(concentrated)
		print "\t[%s] write concentrated src ip to 'src_ip.txt'" % interface
	src_ip_txt.close()
	colored_log("\n=== FINISHED ===", bcolors.HEADER)

if __name__ == '__main__':
	main_loop()