"""
Sample pyATS Easypy job file for interface testing.

Example:
    pyats run job interface_job.py --testbed-file <your tb file>

Arguments:
    --testbed-file: Path and filename of the pyATS testbed file
"""
import os
import logging
from pyats.easypy import run  # pylint: disable=no-name-in-module
from pyats.topology import loader

logger = logging.getLogger(__name__)

TESTBED_FILE = "all_devices.testbed.yml"
DATAFILE = "combined_datafile.yml"
TESTSCRIPT = "test_all.py"

# Find the location of the script in relation to the job file
root_path = os.path.dirname(os.path.abspath(__file__))
datafile_path = os.path.join(root_path, "datafiles")
testbed_path = os.path.join(root_path, "testbeds")
test_path = os.path.join(root_path, "tests")

# Define the testscript to execute
# testscript = os.path.join(test_path, "test_device.py")
TESTSCRIPT = os.path.join(test_path, TESTSCRIPT)

TESTBED = loader.load(os.path.join(testbed_path, TESTBED_FILE))

# Define the datafile containing expected test parameters
DATAFILE = os.path.join(datafile_path, DATAFILE)


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
        datafile=DATAFILE,
        runtime=runtime)
