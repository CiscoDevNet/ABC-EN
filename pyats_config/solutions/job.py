"""
Sample pyATS Easypy job file for interface testing.

Example:
    pyats run job interface_job.py --testbed-file <your tb file>

Arguments:
    --testbed-file: Path and filename of the pyATS testbed file
"""
import argparse
import os
import logging
from pyats.easypy import run  # pylint: disable=no-name-in-module
from pyats.topology import loader

logger = logging.getLogger(__name__)

test_scripts = {
    "ntp": {
        "testbed": "ntp_testbed.yml",
        "script": "test_ntp.py",
        "datafile": "ntp_datafile.yml"
    },
    "lldp": {
        "testbed": "lldp_testbed.yml",
        "script": "test_lldp.py",
        "datafile": "interface_datafile.yml"
    },
    "interfaces": {
        "testbed": "interface_testbed.yml",
        "script": "test_interfaces.py",
        "datafile": "interface_datafile.yml"
    },
    "all": {
        "testbed": "tests/combined_testbed.yml",
        "script": "test_all.py",
        "datafile": "combined_datafile.yml"
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
test_path = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.join(test_path, "tests")

# Define the testscript to execute
# testscript = os.path.join(test_path, "test_device.py")
testscript = os.path.join(test_path, test_script["script"])
testbed = loader.load(test_script["testbed"])

# Define the datafile containing expected test parameters
datafile = os.path.join(test_path, test_script["datafile"])


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
    run(testbed=testbed,
        testscript=testscript,
        datafile=datafile,
        runtime=runtime)
