import requests
import urllib3

urllib3.disable_warnings()

url = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospfv3:ospfv3"

payload = {"Cisco-IOS-XE-ospfv3:ospfv3": [
        {
            "id": <TODO>,
            "address-family": {"ipv6": {"unicast": {"default-information": {"originate": {"always": [None]}}}}}
        }
    ]}
headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

response = requests.request("<TODO>", url, auth=("developer", "1234QWer!"), json=payload, headers=headers, verify=False)

print(response.status_code)

