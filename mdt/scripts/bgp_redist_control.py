#!/usr/bin/env python3

import argparse
from os.path import basename
from connection_defs import providers as devices
from netmiko import ConnectHandler

redist_interface = "Loopback99"

if "inject" in basename(__file__):
    loopback_command = "no shutdown"
    task_type = "inject"
else:
    loopback_command = "shutdown"
    task_type = "retract"

config_commands = [
    f"interface {redist_interface}",
    loopback_command
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
            print(f"{task_type.capitalize()} BGP prefixes from provider-rtr to '{device}'...")
            ssh_conn = ConnectHandler(**devices[device])
            output = ssh_conn.send_config_set(config_commands)
            print(f"\t{task_type.capitalize()} process complete.")

        except KeyError:
            print(f"No connection defined for '{args.target_device}'. Verify device name and retry")
