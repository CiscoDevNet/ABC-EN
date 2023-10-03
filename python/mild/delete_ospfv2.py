import requests

url = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/router/"

headers = {
    "accept": "application/yang-data+json"
}

response = requests.<TODO>(url, headers=headers, auth=("developer", "1234QWer!"), verify=False)

print(response.text)