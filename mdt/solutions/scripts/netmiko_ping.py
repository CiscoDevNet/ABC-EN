import argparse
from netmiko import ConnectHandler

traffic_time = 60  # seconds

devices = {
    "inet-rtr1": {
        "device_type": "cisco_ios",
        "host": "inet-rtr1",
        "username": "developer",
        "password": "1234QWer!"
    },
    "inet-rtr2": {
        "device_type": "cisco_ios",
        "host": "inet-rtr2",
        "username": "developer",
        "password": "1234QWer!"
    }
}

config_commands = [
    f"ip sla schedule 1 start-time now life {traffic_time}",
    f"ip sla schedule 2 start-time now life {traffic_time}"
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        "-device",
                        "--device",
                        action="store",
                        dest="target_device",
                        nargs="+",
                        required=True)
    args, _ = parser.parse_known_args()

    for device in args.target_device:
        try:
            print(f"Generating traffic to provider-rtr from '{device}'...")
            ssh_conn = ConnectHandler(**devices[device])
            output = ssh_conn.send_config_set(config_commands)
            if "cannot modify" in output.lower():
                print("\tTraffic already being generated, try again in 60 seconds.")
            else:
                print(f"\tOK - Traffic will be generated for {traffic_time} seconds.")

        except KeyError:
            print(f"No connection defined for '{args.target_device}'. Verify device name and retry")
