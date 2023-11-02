"""
Example pyATS test using the AEtest automation harness and Easypy
runtime environment for interface state testing.

The job script (interface_job.py) initializes the testbed, triggers
this testscript, and handles generation of HTML logs for task
execution.
"""
# pylint: disable=no-self-use, too-few-public-methods, too-many-branches, line-too-long
import logging
from pyats import aetest
from genie.abstract import Lookup
from genie.libs import ops
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Initialize logging
logger = logging.getLogger(__name__)

# If no shutdown state defined for an interface, set a default
# False = "no shutdown"
# True = "shutdown"
UNSPECIFIED_SHUTDOWN_STATE = False


class CommonSetup(aetest.CommonSetup):
    """
    Common setup tasks - this class can only be instantiated one time per
    testscript.
    """

    @aetest.subsection
    def connect(self, testbed):
        """
        First setup task: connect to all devices in the testbed

        :param testbed: Testbed object passed as a parameter from the Easypy
        job file.
        :return: None (no return defined)
        """
        testbed.connect(log_stdout=False)

    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        """
        The test will be executed against every device in the testbed, so
        define a variable named "device_name" which stores the list of
        devices from the testbed.

        Each iteration of the marked Testcase will be passed the parameter
        "device_name" with the current device's testbed object.

        :param testbed: Testbed object passed as a parameter from the Easypy
        job file.
        :return: None (no return defined)
        """
        aetest.loop.mark(TestOspfv3, device_name=testbed.devices)


class TestOspfv3(aetest.Testcase):
    """
    Main Testcase.  Perform checks against desired vs configured interface
    state on the IOSXE platform.
    """

    # Create 'device' attribute which will be initialized with the pyATS
    # device object during setup.  Any future reference to the device will
    # be made using "self.device" instead of passing the device parameter
    # or repeating "device = testbed.devices[device_name]" in each test.
    device = None

    @aetest.setup
    def setup(self, testbed, device_name):
        """
        Initial setup tasks for this Testcase.  Tasks performed:
            - Initialize the object attribute "device" as a reference to the
              testbed device object for the current host.
            - Mark the "test_interface" method for looping where method
              parameter "interface_name" will represent the currently
              iterated interface's name.

        :param testbed: Easypy-passed testbed object
        :param device_name: Current device as loop-marked by CommonSetup

        :return: None (no return)
        """
        self.device = testbed.devices[device_name]

    @aetest.test
    def test_ospf_running_state(self, steps):
        try:
            parsed_state = self.device.parse("show ospfv3")
        except SchemaEmptyParserError:
            parsed_state = None

        if hasattr(self.device.custom, "ospfv3"):
            # Set the desired state stuff for comparison
            desired_process_id = self.device.custom.ospfv3.get("process_id")
            logger.info("Desired process ID: %s", desired_process_id)

            desired_router_id = self.device.custom.ospfv3.get("router_id")
            logger.info("Desired router ID : %s", desired_router_id)

            with steps.start("Test OSPFv3 running and IPv6 AF is enabled") as step:
                assert parsed_state, "OSPFv3 is not running on the device."  # Even if the process is defined but no AF, it will return null for 'show ospfv3' - OK
                assert parsed_state["vrf"].get(None) is not None, "OSPFv3 is not enabled for the global routing table"
                assert parsed_state["vrf"][None]["address_family"].get("ipv6") is not None, "OSPFv3 IPv6 AF is not enabled"

            configured_state = parsed_state["vrf"][None]["address_family"]["ipv6"]["instance"]

            with steps.start("Test process ID...") as step:
                logger.info("Testing that desired process ID '%s' is in configured process(es): %s", str(desired_process_id), configured_state.keys())
                assert str(desired_process_id) in configured_state, "Process not in configured state"

            with steps.start("Test router ID...") as step:
                if desired_router_id:
                    logger.info("Testing that desired router ID: '%s' matches configured: '%s'", desired_router_id, configured_state[str(desired_process_id)].get("router_id"))
                    assert configured_state[str(desired_process_id)].get("router_id") == str(desired_router_id), "Router ID does not match"
                else:
                    step.skipped("No desired router ID defined, skipping...")
        else:
            # If you want compliance reports, check that NO ospf processes are
            # running - otherwise, PASSX (?) with verbose messages that the device
            # is not in compliance with desired state.
            if not parsed_state:
                self.passed("No desired OSPFv3 configuration, no processes running on the device.")
            else:
                self.passx("No desired OSPFv3 configuration but OSPFv3 is running on the device.")

    @aetest.test
    def test_ospf_area_config(self, steps):
        """
        VERY basic test to see if a stub or NSSA area has been defined
        """
        ospf_running_config = self.device.api.get_running_config_section("router ospfv3")
        ospf_running_config = [x.strip() for x in ospf_running_config]

        if self.device.custom.ospfv3.get("areas") is None:
            self.skipped("No desired state defined for OSPFv3 areas...")
        else:
            for area in self.device.custom.ospfv3.get("areas"):
                logger.error("Area config:\n%s", area)
                if "stub" in area:
                    logger.error("Stub found...")
                    desired_area_config = f"area {area['area_id']} stub"
                    logger.error("Created area config: %s", desired_area_config)
                    if area["stub"].get("no_summary"):
                        desired_area_config += " no-summary"

                elif "nssa" in area:
                    desired_area_config = f"area {area['area_id']} nssa"
                    if area["nssa"].get("no_summary"):
                        desired_area_config += " no-summary"

                assert desired_area_config in ospf_running_config, f"Area {area['area_id']} not present in running-config"

    @aetest.test
    def test_ospf_interface_config(self, steps):
        try:
            parsed_config = self.device.parse(f"show ospfv3 {self.device.custom.ospfv3['process_id']} interface")
        except SchemaEmptyParserError:
            logger.error("No OSPFv3 interfaces are configured")

        for interface in self.device.interfaces:
            with steps.start(interface, continue_=True) as step:
                if not (desired_config := getattr(self.device.interfaces[interface], "ospfv3", None)):
                    step.skipped("No OSPFv3 desired state defined for this interface")
                else:
                    desired_network_type = desired_config.get("network_type")
                    logger.error("Desired network: %s", desired_network_type)
                    interface_op_state = parsed_config["interfaces"].get(interface)
                    assert interface_op_state is not None, "Interface is not configured for OSPFv3"
                    assert interface_op_state["pid"] == desired_config["process_id"], f"Process ID does not match. Expected: {desired_config['process_id']} but actual is {interface_op_state['pid']}."
                    assert interface_op_state["area"] == desired_config["area_id"], f"Area ID does not match. Expected: {desired_config['area_id']} but actual is {interface_op_state['area']}."

                    if desired_network_type:
                        desired_network_type = desired_network_type.replace("-", "_").upper()
                        assert interface_op_state["network_type"] == desired_network_type, f"Network type mismatch. Expected '{desired_network_type}', ops is '{interface_op_state['network_type']}'"


                    logger.error(parsed_config)
                    # with step.start("Test area membership") as substep:

                    # logger.error("Interface ospf config:\n%s", dir(self.device.interfaces[interface].ospfv3))

                #
                # logger.error(parsed_config)

                # with step.start("Check area assignment") as substep:





#
# class CommonCleanup(aetest.CommonCleanup):
#     """
#     Common cleanup tasks - this class can only be instantiated one time per
#     testscript.
#     """
#
#     @aetest.subsection
#     def disconnect(self, testbed):
#         """
#         Disconnect from all testbed devices
#
#         :param testbed: Easypy-passed testbed object
#         :return: None (no return value)
#         """
#         testbed.disconnect()
