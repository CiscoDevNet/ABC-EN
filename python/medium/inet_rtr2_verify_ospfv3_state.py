"""This script verifys the state of OSPFv3"""
import requests
<TODO DISABLE WARNINGS>

<TODO DISABLE WARNINGS>

URL = "https://<TODO>/restconf/data/<TODO>"

PAYLOAD = ""

headers = {
    "accept": "application/<TODO>"
}

response = requests.<TODO>(<TODO>,
                           <TODO>,
                           <TODO>,
                           <TODO>,
                           <TODO>)

print(response.<TODO>)
