import requests
import urllib3

urllib3.disable_warnings()

url = "https://inet-rtr2:443/restconf/data/Cisco-IOS-XE-ospf-oper:ospf-oper-data/ospfv3-router"

payload = ""

headers = {
    "accept": "application/yang-data+json"
}

response = requests.get(url, headers=headers, auth=("developer", "1234QWer!"), verify=False)

print(response.text)