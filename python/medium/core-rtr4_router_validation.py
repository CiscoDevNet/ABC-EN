import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

url = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/<TODO>"

headers = {
    "accept": "application/<TODO>",
    "Content-Type": "application/<TODO>"
}

response = requests.request("<TODO>", <TODO>, <TODO>, <TODO>, <TODO>)

print(response.status_code)
print(response.<TODO>)

