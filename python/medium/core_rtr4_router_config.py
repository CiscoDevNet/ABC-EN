"""This script configures the router for OSPFv3"""
import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

URL = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/"\
      "<TODO>"

payload = {"Cisco-IOS-XE-ospfv3:ospfv3": [
        {
            "id": <TODO>,
            "address-family": {"ipv6": {"unicast": {
                        "area-config": [
                            {
                                "area-id": <TODO>,
                                "stub": {"<TODO>": [None]}
                            }
                        ],
                        "default-information": {"<TODO>": {}}
                    }}}
        }
    ]}

headers = {
    "accept": "application/<TODO>",
    "Content-Type": "application/<TODO>"
}

response = requests.request("<TODO>",
                            <TODO>,
                            <TODO>,
                            <TODO>,
                            <TODO>,
                            <TODO>,
                            <TODO>)

print(response.status_code)

