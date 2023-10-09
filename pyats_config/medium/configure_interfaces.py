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
            device.api.config_link_local_ip_on_interface(interface=interface_name,
                                                         ipv6_address=interface.ipv6_link_local)

        print("\t\tBuilding interface configuration")
        interface.build_config(apply=True)

    # Save the running config
    if SAVE_CONFIG:
        device.api.save_running_config_configuration()

    print("*" * 78)

print("Disconnecting from all devices...")
testbed.disconnect()
