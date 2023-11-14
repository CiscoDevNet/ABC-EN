"""This script validates the OSPFv3 router configuration"""
import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

URL = "https://<TODO>/restconf/data/Cisco-IOS-XE-native:native/"\
      "<TODO>"

payload = {}

headers = {
    "accept": "application/<TODO>n",
    "Content-Type": "application/<TODO>"
}

response = requests.request("<TODO>",
                            <TODO>,
                            <TODO>,
                            <TODO>,
                            <TODO>,
                            <TODO>)

print(response.status_code)
print(response.<TODO>)
