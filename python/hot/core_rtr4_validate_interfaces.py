"""This script validates the OSPFv3 interface configuration"""
<TODO IMPORT REQUIRED LIBARIES>

<TODO DISABLE WARNINGS>

interface_list = [
    <TODO REMAINING INTERFACES>
]

headers = {
    <TODO>
}        

for interface in <TODO>:
    url = <TODO>

    response = <TODO>

    print(f"Stauts code { response.status_code } for { url }")
    print<TODO>