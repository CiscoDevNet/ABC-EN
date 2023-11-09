"""
Connection definitions for each device in the lab. This will not be used
during the DDL; supports scripts that must interact with the lab devices
for purposes such as traffic generation.
"""
devices = {
    "inet-rtr1": {
        "device_type": "cisco_ios",
        "host": "inet-rtr1",
        "username": "developer",
        "password": "1234QWer!"
    },
    "inet-rtr2": {
        "device_type": "cisco_ios",
        "host": "inet-rtr2",
        "username": "developer",
        "password": "1234QWer!"
    }
}

providers = {
    "inet-rtr1": {
        "device_type": "cisco_ios",
        "host": "provider-rtr1",
        "username": "developer",
        "password": "1234QWer!"
    },
    "inet-rtr2": {
        "device_type": "cisco_ios",
        "host": "provider-rtr2",
        "username": "developer",
        "password": "1234QWer!"
    }
}
