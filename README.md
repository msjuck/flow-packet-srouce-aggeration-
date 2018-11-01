
# flow-packet-srouce-aggeration

## What is flow-packet-srouce-aggeration?

This is a script for what devices are sending flow packets to a server that this script running on.

## pre requirements

intstall python > 2.5
install tcpdump
install ip

## how to run?

run Extract pcap from tcpdump


	[07:44:24 root@choi PYUTIL]python find_interface.py


	=== [Stage1] Extract Interface and IP ===


		<Interface List>
		[eno1]:10.20.30.40
		[eno2]:10.20.30.40
		[eno3]:10.20.30.40


	=== [Stage2] TCPDUMP Each Interfaces with Multi-Processing ===


		[Create TCPDUMP Process]: eno1
		[Create TCPDUMP Process]: eno2
		[Create TCPDUMP Process]: eno3
		[TCPDUMP 12324] tcpdump -i eno2 -w eno2.pcap -c 100
		[TCPDUMP 12325] tcpdump -i eno3 -w eno3.pcap -c 100
		[TCPDUMP 12323] tcpdump -i eno1 -w eno1.pcap -c 100
	tcpdump: listening on eno2, link-type EN10MB (Ethernet), capture size 262144 bytes
	tcpdump: tcpdump: listening on eno1, link-type EN10MB (Ethernet), capture size 262144 bytes
	listening on eno3, link-type EN10MB (Ethernet), capture size 262144 bytes
	100 packets captured
	100 packets received by filter
	0 packets dropped by kernel
	100 packets captured
	101 packets received by filter
	0 packets dropped by kernel
		<TCP Dump Process Status>
			[PID12323] : interface <eno1:10.20.30.40> Status : finished
			[PID12324] : interface <eno2:10.20.30.40> Status : finished
			[PID12325] : interface <eno3:10.20.30.40> Status : running
		<TCP Dump Process Status>
			[PID12323] : interface <eno1:10.20.30.40> Status : finished
			[PID12324] : interface <eno2:10.20.30.40> Status : finished
			[PID12325] : interface <eno3:10.20.30.40> Status : running
	100 packets captured
	100 packets received by filter
	0 packets dropped by kernel
		<TCP Dump Process Status>
			[PID12323] : interface <eno1:10.20.30.40> Status : finished
			[PID12324] : interface <eno2:10.20.30.40> Status : finished
			[PID12325] : interface <eno3:10.20.30.40> Status : finished


	=== [Stage3] analyze dump files ===


	Running as user "root" and group "root". This could be dangerous.
		[eno1] write concentrated src ip to 'src_ip.txt'
	Running as user "root" and group "root". This could be dangerous.
		[eno2] write concentrated src ip to 'src_ip.txt'
	Running as user "root" and group "root". This could be dangerous.
		[eno3] write concentrated src ip to 'src_ip.txt'

	=== FINISHED ===
	[07:44:40 root@choi PYUTIL]

and check the src_ip.txt file
