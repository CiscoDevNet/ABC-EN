"""
pyATS testscript for testing LLDP configuration / operational state.

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

# pylint: disable=too-few-public-methods, line-too-long
import logging
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
        aetest.loop.mark(TestLldp, device_name=testbed.devices)


class TestLldp(aetest.Testcase):
    """
    LLDP Testcase.
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
        :param device_name: Current device name as loop-marked by CommonSetup
        :return: None
        """
        self.device = testbed.devices[device_name]

    @aetest.test
    def learn_lldp(self):
        """
        Learn the LLDP operational details from the current device. Moved
        from setup() to ensure this task runs each time, even when the test
        class is inherited.

        :return: None
        """
        self.device.lldp = self.device.learn("lldp")

    @aetest.test
    def test_lldp_running_state(self):
        """
        Test the global LLDP running state against the desired state defined
        by testbed device custom attribute "lldp_enabled"

        :return: None
        """
        state_text = {
            True: "enabled",
            False: "disabled"
        }

        try:
            desired_lldp_state = self.device.custom.lldp_enabled
        except AttributeError:
            self.skipped("No desired state defined for global LLDP state.")

        try:
            operational_state = self.device.lldp.info["enabled"]
        except AttributeError:
            operational_state = False

        assert desired_lldp_state is operational_state, \
            (f"Desired: '{state_text[desired_lldp_state]}', "
             f"Operational: '{state_text[operational_state]}'")

    @aetest.test
    def test_lldp_interfaces(self, steps):
        """
        Compare each interface LLDP state to the desired state (tx/rx) as
        defined by interface custom attribute "lldp_enabled"

        This test is NOT checking individual LLDP parameters such as transmit
        and receive for a specific interface. If either transmit or receive
        are disabled, pyATS will return "False" for the enabled state.

        :param steps: pyATS built-in steps object
        :return: None
        """
        state_text = {
            True: "enabled",
            False: "disabled"
        }

        for interface in self.device.interfaces.values():
            with steps.start(interface.name, continue_=True) as step:
                try:
                    desired_state = interface.lldp_enabled
                except AttributeError:
                    step.skipped("No LLDP desired state defined for interface")

                # Ignore non-ethernet interfaces e.g. Loopback
                if "ethernet" not in str(interface.name).lower():
                    step.skipped("Non-ethernet interface, skipping")

                try:
                    operational_state = self.device.lldp.info["interfaces"][interface.name]["enabled"]
                except AttributeError:
                    operational_state = False

                assert desired_state is operational_state, \
                    (f"Desired: '{state_text[desired_state]}', "
                     f"Operational: '{state_text[operational_state]}'")


class CommonCleanup(aetest.CommonCleanup):
    """
    Common cleanup tasks - this class can only be instantiated one time per
    testscript.
    """

    @aetest.subsection
    def disconnect(self, testbed):
        """
        Disconnect from all testbed devices

        :param testbed: pyATS testbed object
        :return: None
        """
        testbed.disconnect()
