"""
Script demonstrating the use of pyATS "build_config" method to configure
interfaces based on definitions in the testbed file.

Attributes of interfaces which may be configured are accessible inside the
interface "for" loop using dir(interface).  Any attribute listed that is
specified in the testbed and assigned a value will be applied to the device,
assuming "apply=True" is passed to build_config.
"""
from pyats.topology import loader

TESTBED = "testbed.yml"

# Should the running-config be saved after configuration?
SAVE_CONFIG = False

testbed = loader.load(TESTBED)

print("*" * 78)
for device_name, device in testbed.devices.items():
    print(f"Connecting to device '{device_name}'")
    device.connect(log_stdout=False)

    device.api.configure_ospfv3(**device.custom.ospfv3)

    for interface_name, interface in device.interfaces.items():
        # if hasattr(interface, "ospfv3_pid") and hasattr(interface, "ospfv3_area"):
        try:
            device.api.configure_ospfv3_on_interface(interface_name, pid=interface.ospfv3_pid_blah, area=interface.ospfv3_area_blah)
        except AttributeError as err:
            print(f"Can't configure OSPFv3 - missing attribute: {err}")

            if "Loopback" not in interface_name:
                device.api.configure_ospfv3_network_point(interface=interface_name)
        # else:
        #     print("Can't get this, yo")


    print(f"Disconnecting from '{device_name}'")
    device.disconnect()
    print("*" * 78)