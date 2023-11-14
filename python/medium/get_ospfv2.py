"""This script gathers the current state of OSPF"""
import requests

URL = "https://<TODO>/restconf/data/<TODO>"

headers = {
    "accept": "application/<TODO>"
}

response = requests.<TODO>(<TODO>,
                           <TODO>,
                           <TODO>,
                           <TODO>,
                           <TODO>)

print(response.<TODO>)
