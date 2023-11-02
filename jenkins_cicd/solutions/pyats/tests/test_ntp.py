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
        aetest.loop.mark(TestNtp, device_name=testbed.devices)


class TestNtp(aetest.Testcase):
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
    def test_ntp_source_interface(self, ntp_source):
        try:
            desired_source_interface = ntp_source[self.device.name]
            configured_source_interface = self.device.api.get_ntp_source_interface_ip()
        except AttributeError:
            self.failed("No NTP source interface defined in testbed.")

        try:
            assert desired_source_interface in configured_source_interface, \
                "Check desired NTP source interface"
        except TypeError:  # Raised if the configured interface is "None"
            self.failed("No source interface configured on device")
        except AssertionError:  # Raised if the test fails
            self.failed(
                f"Configured NTP source '{configured_source_interface[1]}' "
                f"does not match desired '{self.device.custom.ntp_source}'"
            )
        else:  # Test success - pass!
            self.passed(
                f"Configured NTP source '{configured_source_interface[1]}' "
                f"matches desired '{self.device.custom.ntp_source}'"
            )

    @aetest.test
    def test_ntp_servers(self, steps, ntp_servers):
        try:
            desired_ntp_servers = ntp_servers[self.device.name]
            parse_result = self.device.parse("show ntp config")
            configured_ntp_servers = parse_result['vrf']['default']['address'].keys()
        except AttributeError:
            self.failed("No NTP servers defined in datafile.")
        except SchemaEmptyParserError:
            self.failed("No NTP servers configured on device.")

        for ntp_server in desired_ntp_servers:
            with steps.start(ntp_server, continue_=True) as step:
                try:
                    assert ntp_server.upper() in configured_ntp_servers, \
                        "NTP server not present in configuration"
                except AssertionError:
                    step.failed("NTP server not present in running configuration")
                else:
                    step.passed("NTP server present in running configuration")


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
