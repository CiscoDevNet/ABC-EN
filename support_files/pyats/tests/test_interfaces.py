"""
pyATS testscript for testing interface configuration / operational state.

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
from genie.metaparser.util.exceptions import SchemaEmptyParserError  # pylint: disable=no-name-in-module

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
        aetest.loop.mark(TestInterfaces, device_name=testbed.devices)


class TestInterfaces(aetest.Testcase):
    """
    Interface testcase.
    """

    # Create attributes which will be initialized with the pyATS
    # device object during setup.  Any future reference will be made
    # using "self.attribute" instead of passing the parameter or repeating
    # code like "device = testbed.devices[device_name]" in each test.
    device = None
    interface_global_ops_state = None
    interface_ipv6_ops_state = None

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
    def mark_tests_for_looping(self):
        """
        Mark the interface state test for looping so each step is run for
        every interface in the topology.

        :return: None
        """
        aetest.loop.mark(
            self.test_interface_state,
            interface_name=self.device.interfaces.keys()
        )

    @aetest.test
    def get_interface_operational_state(self):
        """
        Get all the interface operational state one time to speed up tests.

        :return: None
        """
        # All interface operational state
        try:
            self.interface_global_ops_state = self.device.parse("show interfaces")
        except SchemaEmptyParserError:
            self.interface_global_ops_state = {}

        # Interface IPv6 ops state
        try:
            self.interface_ipv6_ops_state = self.device.parse("show ipv6 interface")
        except SchemaEmptyParserError:
            self.interface_ipv6_ops_state = {}

    @aetest.test
    def test_interface_state(self, steps, interface_name):
        """
        Perform tests against the current interface.  The following test logic
        is implemented:
          - Validate interface admin state (shutdown?)
          - Validate the interface description if defined in the testbed
          - Check configured interface IPv6 link-local address matches desired
          - Check configured interface IPv6 address/prefix matches the desired

        If no desired state is defined for a step, that step will be marked as
        SKIPPED.

        Note: ideally, each step in the function would be separate tests. The
        reason for combining tests into one function as steps is for human
        readability in reports, so all tests are grouped per interface.

        :param interface_name: pyATS testbed interface name marked for looping
        :param steps: pyATS built-in steps object
        :return: None
        """
        # Set the current interface object for easy access in the test
        current_interface = self.device.interfaces[interface_name]

        # Prepare the desired state variables
        desired_enable_state = getattr(current_interface, "enabled")
        desired_description = getattr(current_interface, "description")
        desired_ipv6_link_local = getattr(current_interface, "ipv6_link_local", None)
        desired_ipv6_address = getattr(current_interface, "ipv6", None)

        # Prepare the operational state variables
        interface_ops_data = self.interface_global_ops_state.get(current_interface.name, {})
        interface_ipv6_data = self.interface_ipv6_ops_state.get(current_interface.name, {})

        ops_enable_state = interface_ops_data.get("enabled", None)
        ops_description = interface_ops_data.get("description", None)
        ops_ipv6_addresses = interface_ipv6_data.get("ipv6", {})

        # Test 1: Check the admin state.
        with steps.start("Admin state (shutdown)", continue_=True) as step:
            logger.info("Desired: '%s', Operational: '%s'", desired_enable_state, ops_enable_state)
            if not desired_enable_state:
                step.skipped("No desired state defined.")
            assert desired_enable_state is ops_enable_state, \
                (f"Desired: '{desired_enable_state}', "
                 f"Operational: '{ops_enable_state}'")

        # Test 2: Verify the interface description.
        with steps.start("Interface description", continue_=True) as step:
            logger.info("Desired: '%s', Operational: '%s'", desired_description, ops_description)
            if not desired_description:
                step.skipped("No desired state defined.")
            assert desired_description == ops_description, \
                f"Desired: '{desired_description}', Ops: '{ops_description}'"

        # Test 3: Verify the interface IPv6 address.
        with steps.start("Interface IPv6 address", continue_=True) as step:
            logger.info("Desired: '%s'", desired_ipv6_address)
            if not desired_ipv6_address:
                step.skipped("No desired state defined.")
            else:
                desired_ipv6_address = str(desired_ipv6_address).upper()
            assert desired_ipv6_address in ops_ipv6_addresses, \
                f"Desired: '{desired_ipv6_address}' not configured on '{current_interface.name}'"

        # Test 4: Verify the interface IPv6 link local address.
        with steps.start("Interface IPv6 link local address", continue_=True) as step:
            logger.info("Desired: '%s'", desired_ipv6_link_local)
            if not desired_ipv6_link_local:
                step.skipped("No desired state defined.")
            else:
                desired_ipv6_link_local = str(desired_ipv6_link_local).upper()
            assert desired_ipv6_link_local in ops_ipv6_addresses, \
                f"Desired: '{desired_ipv6_link_local}' not configured on '{current_interface.name}'"


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
