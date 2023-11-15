#!/bin/sh
##########################################################################
# Reset all devices to the base state, with no lab-specific configuration
# present. This will erase all running-config and rebuild with management
# VRF and addressing.
# This script should be executed before saving any golden image updates
# to ensure that devices do not retain configuration artifacts.
#
# This is a modified "prepare_lab.sh" script with some tasks stripped
# and some different environment variables set.
#
# Copyright (c) 2023 Cisco and/or its affiliates.
#
# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at
#
#                https://developer.cisco.com/docs/licenses
#
# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.
##########################################################################

# Device to reset - this will be used to load the correct clean file
TARGET_DEVICE=$1

if [ "x${TARGET_DEVICE}" = "x" ]; then
    echo ""
    echo "Unable to continue: missing device name."
    echo ""
    echo "USAGE:"
    echo "    reset_all_devices.sh [device_name | all_devices]"
    echo ""
    echo "Where either a single device name is provided to reset that device"
    echo "or 'all_devices' to reset the full topology"
    exit 1
fi

# Accumulator for any non-true status results
LAB_INIT_RESULT=0

# Obtain the true location of this script
SCRIPT_TRUEPATH="$( readlink -f $0 )"

# Extract the path of this script from the true path
SCRIPT_BASEPATH="$( dirname ${SCRIPT_TRUEPATH} )"
TESTBED_PATH="${SCRIPT_BASEPATH}/testbeds"

# Get the path for the called script (not the true script path)
LAB_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

LAB_PREP_FILE_PATH="${LAB_PATH}/lab_prep_files"
CLEAN_FILE_PATH="${SCRIPT_BASEPATH}/clean_files/startup"
LOG_PATH="${LAB_PREP_FILE_PATH}/logs"

# Python interpreter
PYTHON_VENV=~student/py3venv
PYTHON_BIN=${PYTHON_VENV}/bin/python
PYTHON_PIP_BIN=${PYTHON_VENV}/bin/pip
PYATS_BIN=${PYTHON_VENV}/bin/pyats

# Even though a Python/pyATS binary is explicitly being called from the venv,
# some tools are searching $PATH. Explicitly prepend the path here
PATH=${PYTHON_VENV}/bin:${PATH}

# Set the path that clean files should import to locate the SCP root
# directory when performing full clean/reset ops.
# NOTE: This path is listed here to be easily modified. Later in this script,
# the environment var is added to the pyATS clean execution environment.
TESTBED_SCP_ROOT="${LAB_PREP_FILE_PATH}/device_configs/startup"

# Full path and name of the pyATS testbed and clean file for the lab
PYATS_TESTBED="${TESTBED_PATH}/all_devices.testbed.yml"
PYATS_CLEAN_FILE="${CLEAN_FILE_PATH}/${TARGET_DEVICE}.clean.yml"

if [ ! -f ${PYATS_CLEAN_FILE} ]; then
    echo "Unable to reset device: pyATS clean file is not present"
    echo "Expected: ${PYATS_CLEAN_FILE}"
    exit 1
fi


# Generate the commandline
DEVICE_INIT_CMD="${PYATS_BIN} clean \
    --clean-file ${PYATS_CLEAN_FILE} \
    --testbed-file ${PYATS_TESTBED} \
    --no-upload \
    --no-archive \
    --runinfo-dir ${LOG_PATH} \
    --no-mail"

# Start the lab reset...
echo
echo "******************************************************************************"
echo "Beginning lab device reset tasks..."
echo "******************************************************************************"
echo


if [ -f ${PYATS_CLEAN_FILE} ] && [ -f ${PYATS_TESTBED} ]; then
    # Set the required environment vars and execute the command
    CLEAN_FILE_PATH=${CLEAN_FILE_PATH} \
    DEVICE_CONFIG_PATH="${LAB_PREP_FILE_PATH}/device_configs/startup" \
    TESTBED_SCP_ROOT=${TESTBED_SCP_ROOT} \
    ${DEVICE_INIT_CMD} 2>&1 > ${LOG_PATH}/device_reset.log.txt

    if [ $? -ne 0 ]; then
        LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
    fi
else
    echo "Unable to reset devices. Either the pyATS Testbed or the pyATS clean"
    echo "file (prepare_lab.yml) is not present. If this is unexpected, please contact"
    echo "your instructor."

    LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
fi

if [ ${LAB_INIT_RESULT} -eq 0 ]; then
    echo
    echo "******************************************************************************"
    echo "SUCCESS! Lab device reset completed"
    echo "******************************************************************************"
    echo
else
    echo
    echo "******************************************************************************"
    echo "ERROR - Lab reset encontered problems. Check the logs for details."
    echo "******************************************************************************"
    echo
    exit ${LAB_INIT_RESULT}
fi