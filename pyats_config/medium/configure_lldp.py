"""
Script demonstrating the use of pyATS Genie APIs to configure LLDP on
interfaces based on a custom attribute boolean "lldp_enabled"
"""
from pyats.topology import loader

TESTBED = "lldp_testbed.yml"

# Should the running-config be saved after configuration?
SAVE_CONFIG = False

testbed = loader.load(TESTBED)

print("Connecting to all devices in testbed...")
testbed.connect(log_stdout=False)

print("*" * 78)
for device_name, device in testbed.devices.items():
    print(f"Configuring device '{device_name}'")

    for interface_name, interface in device.interfaces.items():
        if "Loopback" in interface_name:
            print(f"\tSkipping Loopback interface {interface_name}")
            continue

        print(f"\tConfiguring LLDP on interface {interface_name}")

        try:
            if interface.lldp_enabled:
                device.api.configure_lldp_interface(interface=interface_name)
            else:
                print("\t\tLLDP testbed attribute not defined - skipping!")
        except AttributeError as err:
            print("\t\tLLDP state not defined for interface, skipping...")

    # Save the running config
    if SAVE_CONFIG:
        device.api.save_running_config_configuration()

    print("*" * 78)

print("Disconnecting from all devices...")
testbed.disconnect()
