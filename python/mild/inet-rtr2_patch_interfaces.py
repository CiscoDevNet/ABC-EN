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
    if interface == "Loopback=0":
        payload = {
            "Cisco-IOS-XE-ospfv3:ospfv3": {
                "process-id": [
                    {
                        "id": 1,
                        "ipv6": {
                            "area": [
                                {
                                    "id": <TODO>
                                }
                            ]
                        }
                    }
                ]
            }
        }
    else:
        payload = {"Cisco-IOS-XE-ospfv3:ospfv3": {
                "process-id": [
                    {
                        "id": 1,
                        "ipv6": {"area": [{"id": <TODO>}]}
                    }
                ],
                "network-type": {"point-to-point": [None]}
            }}
    
    url = f"https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/interface/{ interface }/Cisco-IOS-XE-ospfv3:ospfv3"

    response = requests.<TODO>(url, headers=headers, json=payload, auth=("developer", "1234QWer!"), verify=False)

    print(f"Stauts code { response.status_code } for { url }")
    print(response.text)