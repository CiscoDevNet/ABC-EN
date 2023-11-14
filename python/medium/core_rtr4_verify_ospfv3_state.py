"""This script validates the OSPFv3 state"""
import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

URL = "https://<TODO>/restconf/data/<TODO>"

PAYLOAD = ""

headers = {
    "accept": "application/<TODO>"
}

response = requests.<TODO>(URL,
                           <TODO>,
                           <TODO>,
                           <TODO>,
                           <TODO>)

print(response.<TODO>)
