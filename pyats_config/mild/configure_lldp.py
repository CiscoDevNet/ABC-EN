"""
Script demonstrating the use of pyATS Genie APIs to configure LLDP on
interfaces based on a custom attribute boolean "lldp_enabled"
"""
from pyats.topology import loader
from unicon.core.errors import SubCommandFailure

TESTBED = ""  # TODO_1 - Specify the testbed file to load

# Should the running-config be saved after configuration?
SAVE_CONFIG = False

testbed = loader.load(TESTBED)

print("Connecting to all devices in testbed...")
testbed.  # TODO_2 - Quietly connect to all devices in the testbed

print("*" * 78)
for device_name, device in testbed.devices.items():
    print(f"Configuring device '{device_name}'")

    for interface_name, interface in device.interfaces.items():
        print(f"\tConfiguring LLDP on interface {interface_name}")
        try:
            if  interface.XXX: # TODO_3 - replace XXX with an interface attribute as a condition
                print("\t\tEnabling LLDP...")
                device.api.  # TODO_4 - use an API to configure the interface
            else:
                print("\t\tDisabling LLDP...")
                device.  # TODO_5 - use an API to unconfigure the interface
        except AttributeError as err:
            print("\t\tLLDP state not defined for interface, skipping...")
        except XXX as err:  # TODO_6: Replace XXX with the proper API exception
            print(f"\t\tUnable to configure LLDP on interface: {err}")

    if device.custom.lldp_enabled:
        print("\tEnabling global LLDP process...")
        device.api.configure_lldp()
        lldp_state = device.parse("")  # TODO_7 - Use the correct parser
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
