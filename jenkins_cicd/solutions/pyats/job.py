"""
Sample pyATS Easypy job file for ABC-EN-A-DDL CI/CD lab.

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

# pylint: disable=invalid-name
import os
import logging
from pyats.easypy import run  # pylint: disable=no-name-in-module
from pyats.topology import loader

logger = logging.getLogger(__name__)

TESTBED_FILE = "all_devices.testbed.yml"
TESTSCRIPT = "test_all.py"

# Find the location of the script in relation to the job file
root_path = os.path.dirname(os.path.abspath(__file__))
testbed_path = os.path.join(root_path, "testbeds")
test_path = os.path.join(root_path, "tests")

# Define the testscript to execute
TESTSCRIPT = os.path.join(test_path, TESTSCRIPT)

TESTBED = loader.load(os.path.join(testbed_path, TESTBED_FILE))


def main(runtime):
    """
    Program entrypoint.

    main() is run automatically when pyATS Easypy starts the job.

    :param runtime: When defined, the Easypy engine automatically passes the
    current runtime object in as an argument.  Includes information about the
    current execution environment, job name, other useful information.

    :return: None (no return)
    """

    # Change the default job name to something useful
    runtime.job.name = "Test device configuration and operational state"

    # Execute the testscript
    run(testbed=TESTBED,
        testscript=TESTSCRIPT,
        runtime=runtime)
