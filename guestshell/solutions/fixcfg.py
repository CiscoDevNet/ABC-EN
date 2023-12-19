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

### TODO: In the final version of the script run in Guestshell, uncomment
###       the following line to import the Cisco CLI module.

import cli

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

### TODO: In the final version of the script run in Guestshell, uncomment
###       the line below to collect the real "show ip interface brief"
###       output and store it in the ResultLines variable.  During the
###       development phase of this script, use the ResultLines populated
###       with a sample output above.

ResultLines = cli.cli(GETIFACESCMD)

Ifaces = []
for Line in ResultLines.splitlines():
    try:
        Ifaces += [IfaceNameMatcher.match(Line).group(1)]
    except AttributeError:
        pass

Config = []
for Iface in Ifaces:
    print(f"Preparing configuration for {Iface}")
    Config += [ f"interface {Iface}", "no ipv6 redirects", "ipv6 nd prefix default no-advertise" ]

print("\nThe script will execute the following sequence of commands:\n")
for Command in Config:
    print("\t", Command)

print("\nApplying the configuration now.")

### TODO: In the final version of the script run in Guestshell, uncomment
###       the following line to execute the configuration commands.

cli.configurep(Config)

exit()
