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
        aetest.loop.mark(TestTelemetry, device_name=testbed.devices)


class TestTelemetry(aetest.Testcase):
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
    def mark_needed_tests(self):
        # aetest.skipIf.affix(section=TestTelemetry,
        #                     condition=not hasattr(self.device.custom, "telemetry"),
        #                     reason="No telemetry custom attribute defined")
        # if hasattr(self.device.custom, "telemetry"):
        aetest.skipIf.affix(section=TestTelemetry.test_telemetry_receivers,
                            condition=not "receivers" in self.device.custom.get("telemetry", {}),
                            reason="No telemetry receivers defined")

        aetest.skipIf.affix(section=TestTelemetry.test_telemetry_subscriptions,
                            condition=not "subscriptions" in self.device.custom.get("telemetry", {}),
                            reason="No telemetry subscriptions defined")
    @aetest.test
    def test_telemetry_receivers(self, steps):
        for receiver in self.device.custom.telemetry["receivers"]:
            with steps.start("Receiver name") as step:
                try:
                    parsed_state = self.device.parse(f"show telemetry receiver name {receiver['name']}")
                except SchemaEmptyParserError:
                    step.failed("Receiver name not configured")
                else:
                    step.passed("Receiver name is configured")

            with steps.start("Receiver address") as step:
                assert parsed_state["name"][receiver["name"]]["host"] == receiver["address"], "Receiver address does not match desired"
            with steps.start("Receiver port") as step:
                assert parsed_state["name"][receiver["name"]]["port"] == receiver["port"], "Receiver port does not match desired"
            with steps.start("Receiver protocol") as step:
                assert parsed_state["name"][receiver["name"]]["protocol"] == receiver["protocol"], "Receiver protocol does not match desired"
            with steps.start("Receiver is valid") as step:
                assert parsed_state["name"][receiver["name"]]["state"].lower() == "valid", "Receiver state is not 'valid', troubleshooting may be required."

        # logger.error("Parsed state:\n%s", parsed_state)
    # {'name': {'telegraf': {'profile': '', 'state': 'Valid', 'state_description': '', 'last_change': '10/19/23 16:47:22', 'type': 'protocol', 'protocol': 'grpc-tcp', 'host': '2001:db8:c15:c0::103', 'port': 57000}}}
    @aetest.test
    def test_telemetry_subscriptions(self, steps):
        try:
            parsed_state = self.device.parse("show telemetry ietf subscription all detail")
        except SchemaEmptyParserError:
            self.failed("No telemetry subscriptions are configured.")

        for subscription in self.device.custom.telemetry.get("subscriptions", []):
            with steps.start(f"Subscription ID: {subscription['id']}") as step:
                assert subscription["id"] in parsed_state["id"], "Subscription ID not in config"
        # with steps.start("Receiver name") as step:
        #     try:
        #         parsed_state = self.device.parse(f"show telemetry receiver name {receiver['name']}")
        #     except SchemaEmptyParserError:
        #         step.failed("Receiver name not configured")
        #     else:
        #         step.passed("Receiver name is configured")

        # with steps.start("Receiver address") as step:
        #     assert parsed_state["name"][receiver["name"]]["host"] == receiver["address"], "Receiver address does not match desired"
        # with steps.start("Receiver port") as step:
        #     assert parsed_state["name"][receiver["name"]]["port"] == receiver["port"], "Receiver port does not match desired"
        # with steps.start("Receiver protocol") as step:
        #     assert parsed_state["name"][receiver["name"]]["protocol"] == receiver["protocol"], "Receiver protocol does not match desired"

        # logger.error("Parsed state:\n%s", parsed_state)
        # logger.error("Testing telemetry subscriptions!")

        #   - id: 11
        #     encoding: encode-kvgpb
        #     xpath: /interfaces-ios-xe-oper:interfaces/interface/statistics
        #     source_vrf: Mgmt-vrf
        #     stream_type: yang-push
        #     update_policy: periodic 500
        #     receiver: telegraf
