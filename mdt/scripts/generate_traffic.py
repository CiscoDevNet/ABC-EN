#!/usr/bin/env python3
"""
Start an IP SLA process to generate traffic from routers to the provider
routers in the MDT lab.
"""
import argparse
from netmiko import ConnectHandler
from connection_defs import devices

TRAFFIC_TIME = 120  # seconds

config_commands = [
    "no ip sla schedule 1",
    f"ip sla schedule 1 start-time now life {TRAFFIC_TIME}",
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
                print(f"\tOK - Traffic will be generated for {TRAFFIC_TIME} seconds.")

        except KeyError:
            print(f"No connection defined for '{args.target_device}'. Verify device name and retry")
