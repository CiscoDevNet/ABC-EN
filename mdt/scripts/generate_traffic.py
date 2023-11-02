#!/usr/bin/env python3

import argparse
from connection_defs import devices
from netmiko import ConnectHandler

traffic_time = 60  # seconds

config_commands = [
    f"ip sla schedule 1 start-time now life {traffic_time}",
    f"ip sla schedule 2 start-time now life {traffic_time}"
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
            print(f"Generating traffic to provider-rtr from '{device}'...")
            ssh_conn = ConnectHandler(**devices[device])
            output = ssh_conn.send_config_set(config_commands)

            if "cannot modify" in output.lower():
                print("\tTraffic already being generated, try again in 60 seconds.")
            elif "not configured" in output.lower():
                print("\tOne or more IPSLA operations is not configured on the device.\n"
                      "\tVerify the configuration and retry")
            else:
                print(f"\tOK - Traffic will be generated for {traffic_time} seconds.")

        except KeyError:
            print(f"No connection defined for '{args.target_device}'. Verify device name and retry")
