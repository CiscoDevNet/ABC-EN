"""
pyATS testscript for testing NTP configuration / operational state.

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
        aetest.loop.mark(TestNtp, device_name=testbed.devices)


class TestNtp(aetest.Testcase):
    """
    NTP testcase.
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
    def test_ntp_source_interface(self):
        """
        Test the configured NTP source matches the desired state as defined
        by testbed device custom attribute "ntp_source"

        :return: None
        """
        try:
            desired_source_interface = self.device.custom.ntp_source
            configured_source_interface = self.device.api.get_ntp_source_interface_ip()
        except AttributeError:
            self.skipped("No desired state defined for NTP source.")

        assert desired_source_interface == configured_source_interface[1], \
            f"Desired: '{desired_source_interface}', Configured: '{configured_source_interface[1]}'"

        logger.info("Desired: '%s', Configured: '%s'",
                    desired_source_interface,
                    configured_source_interface[1])

    @aetest.test
    def test_ntp_servers(self, steps):
        """
        Test configuration / operational state of desired NTP servers defined
        by testbed device custom attribute "ntp_servers"

        :param steps: pyATS built-in steps object
        :return: None
        """
        try:
            desired_ntp_servers = self.device.custom.ntp_servers
            config_parse_result = self.device.parse("show ntp config")
            ntp_server_config = config_parse_result['vrf']['default']['address'].keys()

            # Add operational testing after updating parser to handle IPv6 NTP refid
            # ops_parse_result = self.device.parse("show ntp associations detail")
            # ntp_server_ops = ops_parse_result["vrf"]["default"]["associations"]["address"]
        except AttributeError:
            self.skipped("No desired state defined for NTP servers.")
        except SchemaEmptyParserError:
            self.failed("No NTP servers configured on device.")

        for ntp_server in desired_ntp_servers:
            with steps.start(ntp_server, continue_=True) as step:
                with step.start("Configured state"):
                    assert ntp_server.upper() in ntp_server_config, \
                        "NTP server not present in configuration."

                # Add operational state testing after parser update
                # with step.start("Operational state"):
                #     current_server = \
                #       ntp_server_ops[ntp_server.upper()]["local_mode"]["client"]["isconfigured"]["True"]
                #
                #     # Do something with the operational state...


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
