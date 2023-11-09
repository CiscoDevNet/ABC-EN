"""
Sample pyATS Easypy job file with arguments to select the test(s)
to execute.

Example:
    pyats run job job.py --lldp


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
import argparse
import os
import logging
from pyats.easypy import run  # pylint: disable=no-name-in-module
from pyats.topology import loader

logger = logging.getLogger(__name__)

test_scripts = {
    "ntp": {
        "testbed": "ntp_testbed.yml",
        "script": "test_ntp.py"
    },
    "lldp": {
        "testbed": "lldp_testbed.yml",
        "script": "test_lldp.py"
    },
    "interfaces": {
        "testbed": "interface_testbed.yml",
        "script": "test_interfaces.py"
    },
    "all": {
        "testbed": "tests/combined_testbed.yml",
        "script": "test_all.py"
    }
}

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-n", "--ntp",
                   help="Run NTP tests",
                   action="store_true")
group.add_argument("-l", "--lldp",
                   help="Run LLDP tests",
                   action="store_true")
group.add_argument("-i", "--interfaces",
                   help="Run interface tests",
                   action="store_true")
group.add_argument("-a", "--all",
                   help="Run all tests",
                   action="store_true")
args = parser.parse_args()

for arg in ("ntp", "lldp", "interfaces", "all"):
    if getattr(args, arg):
        test_script = test_scripts[arg]
        break

# Find the location of the script in relation to the job file
base_path = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.join(base_path, "tests")

# Define the testscript to execute
testscript = os.path.join(test_path, test_script["script"])
testbed = loader.load(os.path.join(base_path, test_script["testbed"]))


def main(runtime):
    """
    Program entrypoint.

    main() is run automatically when pyATS Easypy starts the job.

    :param runtime: When defined, the Easypy engine automatically passes the
    current runtime object in as an argument.  Includes information about the
    current execution environment, job name, other useful information.

    :return: None
    """

    # Change the default job name to something useful
    runtime.job.name = "Test device configuration and operational state"

    # Execute the testscript
    run(testbed=testbed,
        testscript=testscript,
        runtime=runtime)
