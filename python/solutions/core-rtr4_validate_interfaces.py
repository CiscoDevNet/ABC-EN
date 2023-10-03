import requests
import urllib3

urllib3.disable_warnings()

interface_list = [
    "GigabitEthernet=2",
    "GigabitEthernet=3",
    "GigabitEthernet=4",
    "GigabitEthernet=5",
    "GigabitEthernet=6",
    "Loopback=0"
]

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}        

for interface in interface_list:
    url = f"https://core-rtr4:443/restconf/data/Cisco-IOS-XE-native:native/interface/{ interface }/Cisco-IOS-XE-ospfv3:ospfv3"

    response = requests.get(url, headers=headers, auth=("developer", "1234QWer!"), verify=False)

    print(f"Stauts code { response.status_code } for { url }")
    print(response.text)