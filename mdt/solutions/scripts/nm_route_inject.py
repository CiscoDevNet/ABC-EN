import argparse
from os.path import basename
from netmiko import ConnectHandler

print(f"\n\nFILE NAME: {basename(__file__)}\n\n")

redist_interface = "Loopback99"

devices = {
    "inet-rtr1": {
        "device_type": "cisco_ios",
        "host": "provider-rtr1",
        "username": "developer",
        "password": "1234QWer!"
    },
    "inet-rtr2": {
        "device_type": "cisco_ios",
        "host": "provider-rtr2",
        "username": "developer",
        "password": "1234QWer!"
    }
}

config_commands = [
    f"interface {redist_interface}",
    "shutdown"
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
            print(f"RAW OUTPUT: {output}")

            if "cannot modify" in output.lower():
                print("\tTraffic already being generated, try again in 60 seconds.")
            elif "not configured" in output.lower():
                print("\tOne or more IPSLA operations is not configured on the device.\n"
                      "\tVerify the configuration and retry")
            else:
                print(f"\tOK - BGP prefixes should be injected.")

        except KeyError:
            print(f"No connection defined for '{args.target_device}'. Verify device name and retry")
