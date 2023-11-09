#!/usr/bin/env python3
"""
Control BGP prefix injection for MDT lab.
"""
import argparse
from os.path import basename
from netmiko import ConnectHandler
from connection_defs import providers as devices

REDIST_INTERFACE = "Loopback99"

if "inject" in basename(__file__):
    LOOPBACK_COMMAND = "no shutdown"
    TASK_TYPE = "inject"
else:
    LOOPBACK_COMMAND = "shutdown"
    TASK_TYPE = "retract"

config_commands = [
    f"interface {REDIST_INTERFACE}",
    LOOPBACK_COMMAND
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        action="store",
                        dest="target_device",
                        nargs="+",
                        required=True,
                        help="Device name(s) to generate traffic from."
                        )
    args, _ = parser.parse_known_args()

    for device in args.target_device:
        print()
        try:
            print(f"{TASK_TYPE.capitalize()} BGP prefixes from provider-rtr to '{device}'...")
            ssh_conn = ConnectHandler(**devices[device])
            output = ssh_conn.send_config_set(config_commands)
            print(f"\t{TASK_TYPE.capitalize()} process complete.")

        except KeyError:
            print(f"No connection defined for '{args.target_device}'. Verify device name and retry")
