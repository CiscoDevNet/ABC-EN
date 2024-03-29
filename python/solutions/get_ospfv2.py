"""This script gathers the current state of OSPF"""
import requests

URL = "https://core-rtr4/restconf/data/Cisco-IOS-XE-native:native/router/"

headers = {
    "accept": "application/yang-data+json"
}

response = requests.get(URL,
                        headers=headers,
                        auth=("developer", "1234QWer!"),
                        verify=False,
                        timeout=60)

print(response.text)
