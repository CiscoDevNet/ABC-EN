import requests
import urllib3
import json

urllib3.disable_warnings()

url = "https://inet-rtr2:443/restconf/data/Cisco-IOS-XE-native:native/router/Cisco-IOS-XE-ospfv3:ospfv3"

payload = {}

headers = {
    "accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

response = requests.request("GET", url, auth=("developer", "1234QWer!"), headers=headers, verify=False)

print(response.status_code)
print(response.json())