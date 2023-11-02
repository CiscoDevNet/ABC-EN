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
        aetest.loop.mark(TestLldp, device_name=testbed.devices)


class TestLldp(aetest.Testcase):
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
        lookup = Lookup.from_device(self.device)

        # Why lldp.lldp.Lldp?
        # Full path is genie.libs.ops.lldp.iosxe.lldp.Lldp
        # Since we have abstracted via Lookup in the setup(), device OS
        # does not need to be specified, nor does genie.libs.
        # So it's ops.lldp.lldp.Lldp
        # Where does device.lib comes from? It's the reference to the
        # Lookup.from_device() from setup().
        self.device.lldp = lookup.ops.lldp.lldp.Lldp(device=self.device)
        self.device.lldp.learn()

    @aetest.test
    def test_lldp_running_state(self, lldp_run):

        lookup = Lookup.from_device(self.device)

        # Why lldp.lldp.Lldp?
        # Full path is genie.libs.ops.lldp.iosxe.lldp.Lldp
        # Since we have abstracted via Lookup in the setup(), device OS
        # does not need to be specified, nor does genie.libs.
        # So it's ops.lldp.lldp.Lldp
        # Where does device.lib comes from? It's the reference to the
        # Lookup.from_device() from setup().
        self.device.lldp = lookup.ops.lldp.lldp.Lldp(device=self.device)
        self.device.lldp.learn()

        logger.error(lldp_run[self.device.name])
        state_text = {
            True: "enabled",
            False: "disabled"
        }

        desired_lldp_state = lldp_run[self.device.name]
        desired_state_text = state_text[desired_lldp_state]

        logger.error("LLDP Info: %s", self.device.lldp)
        try:
            assert self.device.lldp.info["enabled"], "LLDP not enabled"
        except AttributeError:
            if desired_lldp_state:
                self.failed(f"Configured state does NOT match desired state '{desired_state_text}'")
            else:
                aetest.skipIf.affix(section=TestLldp.test_lldp_interfaces, condition=True, reason="LLDP global state disabled")
                self.passed(f"Configured state matches desired state '{desired_state_text}'")
        else:
            if not desired_lldp_state:
                self.failed(f"Configured state does NOT match desired state '{desired_state_text}'")
            else:
                aetest.skipIf.affix(section=TestLldp.test_lldp_interfaces, condition=False)
                self.passed(f"Configured state matches desired state '{desired_state_text}'")


    @aetest.test
    def test_lldp_interfaces(self, steps, lldp_run, lldp_interface):

        state_text = {
            True: "enabled",
            False: "disabled"
        }

        desired_lldp_interface_state = lldp_interface[self.device.name]

        for interface in self.device.interfaces.values():
            if str(interface.name).startswith("Loopback"):
                continue

            try:
                desired_state = desired_lldp_interface_state[interface.name]
                desired_state_text = state_text[desired_state]
            except AttributeError:
                self.failed("Interface is not present in test datafile.")

            try:
                configured_state = self.device.lldp.info["interfaces"][interface.name]["enabled"]
                configured_state_text = state_text[configured_state]
            except AttributeError:
                self.failed("LLDP is not running on the device, cannot determine interface state.")

            with steps.start(interface.name, continue_=True) as step:
                try:
                    assert configured_state is desired_state, "Configured LLDP state does not match desired"
                except AssertionError:
                    step.failed(f"Configured LLDP state '{configured_state_text}' doesn't match desired '{desired_state_text}'")
                else:
                    step.passed(f"Configured LLDP state '{configured_state_text}' matches desired '{desired_state_text}'")


class CommonCleanup(aetest.CommonCleanup):
    """
    Common cleanup tasks - this class can only be instantiated one time per
    testscript.
    """

    @aetest.subsection
    def disconnect(self, testbed):
        """
        Disconnect from all testbed devices

        :param testbed: Easypy-passed testbed object
        :return: None (no return value)
        """
        testbed.disconnect()
