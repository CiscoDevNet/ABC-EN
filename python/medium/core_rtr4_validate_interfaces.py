"""This script validates the OSPFv3 interface configuration"""
import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

interface_list = [
    "GigabitEthernet=2",
    <TODO REMAINING INTERFACES>
]

headers = {
    "accept": "application/<TODO>",
    "Content-Type": "application/<TODO>"
}        

for interface in interface_list:
    url = f"https://<TODO>restconf/data/Cisco-IOS-XE-native:native"
          f"<TODO>"

    response = requests.<TODO>(<TODO>,
                               <TODO>,
                               <TODO>,
                               <TODO>,
                               <TODO>)

    print(f"Stauts code { response.status_code } for { url }")
    print(response.<TODO>)
