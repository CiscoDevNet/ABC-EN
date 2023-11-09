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

TESTBED = ""  # <TODO_1> - Specify the correct extended testbed for this job.

# Should the running-config be saved after configuration?
SAVE_CONFIG = False

testbed = loader.load(TESTBED)

print("Connecting to all devices in testbed...")
testbed.  # <TODO_2> - use the correct method to connect to all devices

print("*" * 78)
for device_name, device in testbed.devices.items():
    print(f"Configuring device '{device_name}'")

    print("\tConfiguring NTP using a template...")
    # <TODO_3> - Replace below placeholder text with the correct Genie API
    device.api.replace_with_genie_api(templates_dir="",  # <TODO_4> - specify templates directory
                                      template_name="",  # <TODO_5> - specify the Jinja2 template
                                      ntp_source=device.custom.REPLACE_THIS,  # <TODO_6> - use a testbed custom attribute for NTP source
                                      ntp_servers=device.custom.REPLACE_THIS)  # <TODO_7> - use a testbed custom attributes for NTP servers

    # Save the running config
    if SAVE_CONFIG:
        device.api.save_running_config_configuration()

    print("*" * 78)

print("Disconnecting from all devices...")
testbed.disconnect()
