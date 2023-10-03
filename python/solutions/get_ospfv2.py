import requests

url = "https://core-rtr4/restconf/data/Cisco-IOS-XE-native:native/router/"

headers = {
    "accept": "application/yang-data+json"
}

response = requests.get(url, headers=headers, auth=("developer", "1234QWer!"), verify=False)

print(response.text)