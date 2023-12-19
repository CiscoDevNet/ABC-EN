#!/usr/bin/python3

'''

The purpose of the script is to configure "no ipv6 redirects" and "ipv6 nd
prefix default no-advertise" on all Ethernet-type (sub)interfaces.  The
script accomplishes this in the following steps:

1.  Using "show ip interface brief" IOS EXEC command, collect the list of
all interfaces.

2.  Using the regular expression matcher from the re module, match all
interface names containing the "Ethernet" substring and store them in a
list.

3.  Iterating through this list, prepare a new list of IOS configuration
mode commands that apply the required configuration across all Ethernet-type
(sub)interfaces.
'''

import re

### TODO: In the final version of the script run in Guestshell, add the 
###       proper Python statement below this comment to import the Cisco CLI
###       module.

IfaceNameMatcher = re.compile(r"([a-zA-Z]*Ethernet[0-9/\.]+)\s+")

GETIFACESCMD="show ip interface brief"

ResultLines = '''
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet1       192.168.10.12   YES NVRAM  up                    up
GigabitEthernet2       unassigned      YES NVRAM  up                    up
GigabitEthernet3       unassigned      YES NVRAM  up                    up
GigabitEthernet4       unassigned      YES NVRAM  up                    up
GigabitEthernet5       unassigned      YES NVRAM  up                    up
GigabitEthernet6       unassigned      YES NVRAM  up                    up
Loopback0              172.16.100.12   YES NVRAM  up                    up
VirtualPortGroup0      unassigned      YES unset  up                    up
'''

### TODO: In the final version of the script run in Guestshell, add the
###       proper Python statement below this comment to execute the IOS EXEC
###       command in the GETIFACESCMD variable, and store the result into
###       the ResultLines variable instead of the sample output above. 
###       During the development phase of this script, use the ResultLines
###       populated with the sample output.

Ifaces = []
for Line in ResultLines.splitlines():
    try:
        Ifaces += [IfaceNameMatcher.match(Line).group(1)]
    except AttributeError:
        pass

Config = []
for Iface in Ifaces:
    print(f"Preparing configuration for {Iface}")
### TODO: In the final version of the script run in Guestshell, add the
###       proper Python statement below this comment to add three new string
###       elements to the Config list:
###       - The interface name in the Iface variable
###       - The "no ipv6 redirects" command
###       - The "ipv6 nd prefix default no-advertise" command

print("\nThe script will execute the following sequence of commands:\n")
for Command in Config:
    print("\t", Command)

print("\nApplying the configuration now.")

### TODO: In the final version of the script run in Guestshell, add the
###       proper Python statement below this comment to execute the
###       configuration mode commands prepared in the Config variable.  With
###       each executed command, print the status of applying it.


exit()
