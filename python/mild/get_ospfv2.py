"""This script gathers the current state of OSPF"""
import requests

URL = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/router/"

headers = {
    "accept": "application/yang-data+json"
}

response = requests.<TODO>(URL,
                           headers=headers,
                           auth=("developer", "1234QWer!"),
                           verify=False,
                           timeout=60)

print(response.text)
