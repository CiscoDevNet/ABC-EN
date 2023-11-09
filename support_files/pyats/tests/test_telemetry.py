"""
pyATS testscript for testing telemetry configuration / operational state.

Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Palmer Sample <psample@cisco.com>"
__copyright__ = "Copyright (c) 2023 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# pylint: disable=line-too-long
import logging
from genie.metaparser.util.exceptions import SchemaEmptyParserError  # pylint: disable=no-name-in-module
from pyats import aetest

# Initialize logging
logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):
    """
    Common setup tasks - this class can only be instantiated one time per
    testscript.
    """

    @aetest.subsection
    def connect(self, testbed):
        """
        First setup task: connect to all devices in the testbed

        :param testbed: Testbed object passed as a parameter from the job file
        :return: None
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

        :param testbed: Testbed object passed as a parameter from the job file
        :return: None
        """
        aetest.loop.mark(TestTelemetry, device_name=testbed.devices)


class TestTelemetry(aetest.Testcase):
    """
    Telemetry testcase.
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

        :param testbed: pyATS testbed object
        :param device_name: Current device as loop-marked by CommonSetup
        :return: None
        """
        self.device = testbed.devices[device_name]

    @aetest.test
    def mark_needed_tests(self):
        """
        Mark tests to be skipped based on desired state

        :return: None
        """
        aetest.skipIf.affix(section=TestTelemetry.test_telemetry_receivers,
                            condition="receivers" not in self.device.custom.get("telemetry", {}),
                            reason="No telemetry receivers defined")

        aetest.skipIf.affix(section=TestTelemetry.test_telemetry_subscriptions,
                            condition="subscriptions" not in self.device.custom.get("telemetry", {}),
                            reason="No telemetry subscriptions defined")

    @aetest.test
    def test_telemetry_receivers(self, steps):
        """
        Test the telemetry receiver config

        :param steps: pyATS built-in steps object
        :return: None
        """
        for receiver in self.device.custom.telemetry["receivers"]:
            try:
                desired_name = receiver["name"]
                desired_receiver_address = receiver["address"]
                desired_receiver_port = receiver["port"]
                desired_receiver_protocol = receiver["protocol"]
            except KeyError as err:
                self.failed(f"Receiver desired state is incomplete / missing required parameters\n"
                            f"Details: {err}")

            with steps.start(f"Receiver '{desired_name}'", continue_=True) as step:
                try:
                    parsed_state = self.device.parse(f"show telemetry receiver name {desired_name}")
                    operational_address = parsed_state["name"][desired_name]["host"]
                    operational_port = parsed_state["name"][desired_name]["port"]
                    operational_protocol = parsed_state["name"][desired_name]["protocol"]
                    operational_status = parsed_state["name"][desired_name]["state"].lower()
                except SchemaEmptyParserError:
                    step.failed("Receiver name not configured")

                with step.start("Receiver address"):
                    assert desired_receiver_address == operational_address, \
                        f"Desired address: '{desired_receiver_address}', Ops: '{operational_address}'"

                with step.start("Receiver port"):
                    assert desired_receiver_port == operational_port, \
                        f"Desired port: '{desired_receiver_port}', Ops: '{operational_port}'"

                with step.start("Receiver protocol"):
                    assert desired_receiver_protocol == operational_protocol, \
                        f"Desired protocol: '{desired_receiver_protocol}', Ops: '{operational_protocol}'"

                with step.start("Operational state"):
                    assert operational_status == "valid", \
                        "Operational state is NOT 'valid', troubleshooting may be required."

    @aetest.test
    def test_telemetry_subscriptions(self, steps):
        """
        Test the telemetry subscriptions match the desired state

        :param steps: pyATS built-in steps object
        :return: None
        """
        # pylint: disable=too-many-locals
        try:
            parsed_state = self.device.parse("show telemetry ietf subscription all detail")
        except SchemaEmptyParserError:
            self.failed("No telemetry subscriptions are configured.")

        for subscription in self.device.custom.telemetry.get("subscriptions", []):
            try:
                desired_id = int(subscription["id"])
                desired_encoding = subscription["encoding"]
                desired_xpath = subscription["xpath"]
                desired_source_vrf = subscription.get("source_vrf", None)
                desired_stream_type = subscription["stream_type"]
                desired_update_trigger, desired_update_period = subscription["update_policy"].split()
                desired_receiver = subscription["receiver"]  # pylint: disable=unused-variable
            except KeyError as err:
                self.failed(f"Receiver desired state is incomplete / missing required parameters\n"
                            f"Details: {err}")

            with steps.start(f"Subscription ID: {desired_id}") as step:
                assert desired_id in parsed_state["id"], \
                    f"Desired ID: '{desired_id}' not present in ops state"

                # NOTE: Receiver information not present in parsed data...
                ops_encoding = parsed_state["id"][desired_id]["encoding"]
                ops_xpath = parsed_state["id"][desired_id]["filter"]["xpath"]
                ops_source_vrf = parsed_state["id"][desired_id].get("source_vrf", None)
                ops_stream_type = parsed_state["id"][desired_id]["stream"]
                ops_update_trigger = parsed_state["id"][desired_id]["update_policy"]["update_trigger"]
                ops_update_period = parsed_state["id"][desired_id]["update_policy"]["period"]
                ops_state = parsed_state["id"][desired_id]["state"].lower()

                with step.start("Encoding"):
                    assert desired_encoding == ops_encoding, \
                        f"Desired: '{desired_encoding}', Ops: '{ops_encoding}'"

                with step.start("xpath"):
                    assert desired_xpath == ops_xpath, \
                        f"Desired: '{desired_xpath}', Ops: '{ops_xpath}'"

                with step.start("Source VRF"):
                    assert desired_source_vrf == ops_source_vrf, \
                        f"Desired: '{desired_source_vrf}', Ops: '{ops_source_vrf}'"

                with step.start("Stream type"):
                    assert desired_stream_type == ops_stream_type, \
                        f"Desired: '{desired_stream_type}', Ops: '{ops_stream_type}'"

                with step.start("Update trigger"):
                    assert desired_update_trigger == ops_update_trigger, \
                        f"Desired: '{desired_update_trigger}', Ops: '{ops_update_trigger}'"

                with step.start("Update period"):
                    assert int(desired_update_period) == int(ops_update_period), \
                        f"Desired: '{desired_update_period}', Ops: '{ops_update_period}'"

                with step.start("Subscription state"):
                    assert ops_state == "valid", \
                        f"Desired: 'valid', Ops: '{ops_state}'"
