"""This script verifys the state of OSPFv3"""
import requests
import urllib3

urllib3.disable_warnings()

URL = "https://inet-rtr2:443/restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospfv3-router"

PAYLOAD = ""

headers = {
    "accept": "application/yang-data+json"
}

response = requests.get(URL,
                        headers=headers,
                        auth=("developer", "1234QWer!"),
                        verify=False,
                        timeout=60)

print(response.text)
