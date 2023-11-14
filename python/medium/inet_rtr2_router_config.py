"""This script configures the router of OSPFv3"""
import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

URL = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/"\
      "<TODO>"

payload = {"Cisco-IOS-XE-ospfv3:ospfv3": [
        {
            "id": <TODO>,
            "address-family": {"<TODO>": {"unicast": {"default-information": {"<TODO>": 
                                                                              {"always": [None]}}}}}
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

print(response.<TODO>)
