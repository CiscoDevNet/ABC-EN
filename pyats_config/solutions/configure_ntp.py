"""
Example script to configure devices using Jinja2 templates with pyATS

Steps:
1. Connect to all devices in the testbed
2. Loop over each device in the testbed
3. Configure the device using a Jinja2 template, passing custom testbed
   parameters to the template for rendering
4. Disconnect from all devices in the testbed
"""
from pyats.topology import loader

TESTBED = "ntp_testbed.yml"

# Should the running-config be saved after configuration?
SAVE_CONFIG = False

testbed = loader.load(TESTBED)

print("Connecting to all devices in testbed...")
testbed.connect()

print("*" * 78)
for device_name, device in testbed.devices.items():
    print(f"Configuring device '{device_name}'")

    print("\tConfiguring NTP using a template...")
    device.api.configure_by_jinja2(templates_dir="templates",
                                   template_name="ntp.j2",
                                   ntp_source=device.custom.ntp_source,
                                   ntp_servers=device.custom.ntp_servers)

    # Save the running config
    if SAVE_CONFIG:
        device.api.save_running_config_configuration()

    print("*" * 78)

print("Disconnecting from all devices...")
testbed.disconnect()
