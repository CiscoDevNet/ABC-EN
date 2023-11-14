"""This script validates the OSPFv3 Interface configuration"""
import requests
import urllib3

urllib3.disable_warnings()

interface_list = [
    "GigabitEthernet=2",
    "GigabitEthernet=3",
    "GigabitEthernet=4",
    "GigabitEthernet=5",
    "Loopback=0"
]

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}        

for interface in interface_list:
    url = f"https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/interface/"\
          f"{ interface }/Cisco-IOS-XE-ospfv3:ospfv3"

    response = requests.<TODO>(url,
                               headers=headers,
                               auth=("developer", "1234QWer!"),
                               verify=False,
                               timeout=60)

    print(f"Stauts code { response.status_code } for { url }")
    print(response.text)
