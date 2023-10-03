import requests
import urllib3

urllib3.disable_warnings()

url = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospfv3:ospfv3"

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

response = requests.request("<TODO>", url, auth=("developer", "1234QWer!"), headers=headers, verify=False)

print(response.status_code)
print(response.json())

