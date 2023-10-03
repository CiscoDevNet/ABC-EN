import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

interface_list = [
    "GigabitEthernet=2",
    <TODO - REMAINING INTERFACES>
]

headers = {
    "accept": "application/<TODO>",
    "Content-Type": "application/<TODO>"
}        

for interface in <TODO>:
    if interface == "<TODO>":
        <TODO> = {
            "Cisco-IOS-XE-ospfv3:ospfv3": {
                "process-id": [
                    {
                        "id": <TODO>,
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
    elif interface == <TODO>
        <TODO> = {"Cisco-IOS-XE-ospfv3:ospfv3": {
                "process-id": [
                    {
                        "id": <TODO>,
                        "ipv6": {"area": [{"id": <TODO>}]}
                    }
                ],
                "network-type": {"<TODO>": [None]}
            }}        
    else:
        <TODO> = {"Cisco-IOS-XE-ospfv3:ospfv3": {
                "process-id": [
                    {
                        "id": <TODO>,
                        "ipv6": {"area": [{"id": <TODO>}]}
                    }
                ],
                "network-type": {"<TODO>": [None]}
            }}
    
    url = f"https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/<TODO>"

    response = requests.<TODO>(<TODO>, <TODO>, <TODO>, <TODO>, <TODO>)

    print(f"Stauts code { response.status_code } for { url }")
    print(<TODO>)