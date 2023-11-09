"""
Script demonstrating the use of pyATS Genie APIs to configure LLDP on
interfaces based on a custom attribute boolean "lldp_enabled"
"""
from pyats.topology import loader
from unicon.core.errors import SubCommandFailure  # pylint: disable=no-name-in-module

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
        print(f"\tConfiguring LLDP on interface {interface_name}")
        try:
            if interface.lldp_enabled:
                print("\t\tEnabling LLDP...")
                device.api.configure_lldp_interface(interface=interface_name)
            else:
                print("\t\tDisabling LLDP...")
                device.api.unconfigure_lldp_interface(interface=interface_name)
        except AttributeError as err:
            print("\t\tLLDP state not defined for interface, skipping...")
        except SubCommandFailure as err:
            print(f"\t\tUnable to configure LLDP on interface: {err}")

    if device.custom.lldp_enabled:
        print("\tEnabling global LLDP process...")
        device.api.configure_lldp()
        lldp_state = device.parse("show lldp interface")
        print(f"\n{device_name} LLDP Operational state:\n\t(interface_name): (tx)/(rx)\n")
        for lldp_interface, interface_state in lldp_state["interfaces"].items():
            print(f"\t{lldp_interface}: {interface_state['tx']}/{interface_state['rx']}")
    else:
        print("\tDisabling global LLDP process...")
        device.api.unconfigure_lldp()

    # Save the running config
    if SAVE_CONFIG:
        device.api.save_running_config_configuration()

    print("*" * 78)

print("Disconnecting from all devices...")
testbed.disconnect()
