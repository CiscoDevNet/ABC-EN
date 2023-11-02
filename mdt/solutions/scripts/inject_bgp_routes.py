import argparse
import requests
from urllib3 import disable_warnings

disable_warnings()

loopback_id = 99

destination_device = {
    "inet-rtr1": "provider-rtr1",
    "inet-rtr2": "provider-rtr2"
}

device_credentials = ("developer", "1234QWer!")

shutdown_payload = {
    "Cisco-IOS-XE-native:shutdown": [
        None
    ]
}

restconf = requests.Session()
restconf.verify = False
restconf.headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}
restconf.auth = device_credentials



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "-device", "--device", action="store", dest="target_device", required=True)
    args, _ = parser.parse_known_args()

    route_source = destination_device[args.target_device]

    print(f"Injecting BGP prefixes from '{route_source}'...")

# for device in destination_devices:
#     url = f"https://{device}/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=99/shutdown"
#     result = restconf.delete(url)
#     print(result.status_code)
#
#     # Shutdown the interface:
#     # result = restconf.put(url, json=shutdown_payload)
#     # print(result.status_code)
