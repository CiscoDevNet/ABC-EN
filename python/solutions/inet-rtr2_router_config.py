import requests
import urllib3

urllib3.disable_warnings()

url = "https://inet-rtr2:443/restconf/data/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospfv3:ospfv3"

payload = {"Cisco-IOS-XE-ospfv3:ospfv3": [
        {
            "id": 1,
            "address-family": {"ipv6": {"unicast": {"default-information": {"originate": {"always": [None]}}}}}
        }
    ]}
headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

response = requests.request("PATCH", url, auth=("developer", "1234QWer!"), json=payload, headers=headers, verify=False)

print(response.status_code)

