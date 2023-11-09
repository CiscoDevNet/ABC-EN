"""
Script demonstrating the use of pyATS "build_config" method to configure
interfaces based on definitions in the testbed file.

Any valid testbed attribute that is associated with a Genie model will be
automatically parsed and applied to the interface configuration, assuming
"apply=True" is passed to the build_config() method.
"""
from pyats.topology import loader

TESTBED = "interface_testbed.yml"

# Should the running-config be saved after configuration?
SAVE_CONFIG = False

testbed = loader.load(TESTBED)

print("Connecting to all devices in testbed...")
testbed.connect(log_stdout=False)

print("*" * 78)
for device_name, device in testbed.devices.items():
    print(f"Configuring device '{device_name}'")

    for interface_name, interface in device.interfaces.items():
        print(f"\tConfiguring interface {interface_name}")

        print("\t\tConfiguring link local address")
        if interface.ipv6_link_local:
            device.api.XXX(interface=interface_name,  # <TODO_1> - replace XXX with an API for link local address
                           ipv6_address=interface.ipv6_link_local)

        print("\t\tBuilding interface configuration")
        print(interface.XXX(apply=False))  # <TODO_2> - replace XXX with the proper method
        # <TODO_3> - Change the above to apply config to the device.

    # Save the running config
    if SAVE_CONFIG:
        device.api.save_running_config_configuration()

    print("*" * 78)

print("Disconnecting from all devices...")
testbed.disconnect()
