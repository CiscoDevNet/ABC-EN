"""
pyATS testscript for testing OSPFv3 configuration / operational state.

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
        aetest.loop.mark(TestOspfv3, device_name=testbed.devices)


class TestOspfv3(aetest.Testcase):
    """
    OSPFv3 Testcase.
    """

    # Create attributes which will be initialized with the pyATS
    # device object during setup.  Any future reference will be made
    # using "self.attribute" instead of passing the parameter or repeating
    # code like "device = testbed.devices[device_name]" in each test.
    device = None
    ospfv3_running_config = None
    ospfv3_global_ops_state = None
    ospfv3_interface_ops_state = None

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
    def get_ospfv3_conf_ops_state(self):
        """
        Initial retrieval of OSPFv3 configuration and operational state for
        testing.

        :return: None
        """
        # This test class initially supports the IPv6 address family in the
        # global routing table. Extract that data here to reduce the number
        # of keys accessed in testcases.
        try:
            parsed_state = self.device.parse("show ospfv3")
            self.ospfv3_global_ops_state = parsed_state["vrf"][None]["address_family"]["ipv6"]["instance"]
        except SchemaEmptyParserError:
            self.ospfv3_global_ops_state = {}

        try:
            desired_pid = self.device.custom.ospfv3.get("process_id", 1)
            self.ospfv3_interface_ops_state = self.device.parse(f"show ospfv3 {desired_pid} interface")
        except SchemaEmptyParserError:
            self.ospfv3_interface_ops_state = {}

        running_config = self.device.api.get_running_config_section("router ospfv3")
        self.ospfv3_running_config = [c.strip() for c in running_config]

    @aetest.test
    def test_ospf_process_id(self):
        """
        Test the desired OSPF process ID is operational

        :return: None
        """
        try:
            desired_process_id = str(self.device.custom.ospfv3["process_id"])
        except (AttributeError, KeyError):
            self.skipped("No desired state defined.")

        running_processes = self.ospfv3_global_ops_state

        assert desired_process_id in running_processes, \
            f"Desired process ID '{desired_process_id}' is not running."

        logger.info("Desired: '%s', Running: '%s'",
                    desired_process_id, list(running_processes.keys()))

    @aetest.test
    def test_ospf_router_id(self):
        """
        Test the desired OSPF router ID is operational for the desired
        process.

        :return: None
        """
        try:
            desired_pid = str(self.device.custom.ospfv3["process_id"])
            desired_router_id = str(self.device.custom.ospfv3["router_id"])
        except (AttributeError, KeyError):
            self.skipped("No desired state defined.")

        try:
            running_router_id = self.ospfv3_global_ops_state[desired_pid]["router_id"]
        except KeyError:
            self.failed("No router ID found in ops state for the requested process.")

        assert desired_router_id == running_router_id, \
            f"Desired: '{desired_router_id}', Running: '{running_router_id}'"

        logger.info("Desired: '%s', Running: '%s'",
                    desired_router_id, running_router_id)

    @aetest.test
    def test_ospf_area_state(self, steps):
        """
        Basic test to check operational state for stub / NSSA areas.

        This is a configuration state check (not ops) because the parser
        doesn't gather area details at this time.

        :param steps: pyATS built-in steps object
        :return: None
        """
        try:
            desired_areas = self.device.custom.ospfv3["areas"]
        except (AttributeError, KeyError):
            self.skipped("No desired state defined.")

        for area in desired_areas:
            with steps.start(f"Area {area['area_id']}", continue_=True):
                if "stub" in area:
                    desired_area_config = f"area {area['area_id']} stub"
                    if area["stub"].get("no_summary"):
                        desired_area_config += " no-summary"
                        logger.info("Testing for total stub area")
                    else:
                        logger.info("Testing for stub area")

                elif "nssa" in area:
                    desired_area_config = f"area {area['area_id']} nssa"
                    if area["nssa"].get("no_summary"):
                        desired_area_config += " no-summary"
                        logger.info("Testing for total NSSA")
                    else:
                        logger.info("Testing for NSSA")

                assert desired_area_config in self.ospfv3_running_config, \
                    f"Desired configuration: '{desired_area_config}' not present"

    @aetest.test
    def test_ospf_interface_config(self, steps):
        """
        Test each interface OSPFv3 ops state to the desired state

        :param steps: pyATS built-in steps object
        :return: None
        """
        for interface in self.device.interfaces:
            with steps.start(interface, continue_=True) as step:
                try:
                    desired_state = getattr(self.device.interfaces[interface], "ospfv3", None)
                    desired_area_id = desired_state["area_id"]
                    desired_process_id = desired_state["process_id"]
                    desired_network_type = desired_state["network_type"].replace("-", "_").upper()
                except AttributeError:
                    step.skipped("No desired state defined.")

                try:
                    operational_state = self.ospfv3_interface_ops_state["interfaces"][interface]
                    running_area_id = operational_state["area"]
                    running_process_id = operational_state["pid"]
                    running_network_type = operational_state["network_type"]
                except KeyError:
                    step.failed("OSPFv3 not operational on interface.")

                assert desired_area_id == running_area_id, \
                    f"Desired area id: '{desired_area_id}', Operational: '{running_area_id}'"

                assert desired_process_id == running_process_id, \
                    f"Desired process ID: '{desired_process_id}', Operational: '{running_process_id}'"

                assert desired_network_type == running_network_type, \
                    f"Desired network type: '{desired_network_type}', Operational: '{running_network_type}'"
