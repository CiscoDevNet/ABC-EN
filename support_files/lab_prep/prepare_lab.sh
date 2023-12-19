#!/bin/sh
##########################################################################
# Initialize lab devices and install prerequisites (if needed).
# Each lab can have an optional local init script located at
# localsetup/local_setup.sh in the lab directory. If present,
# the file will be sourced at the end of this script.
#
# If a requirements.txt file is located in the lab directory, pip will
# attempt to install with the --upgrade option.
#
# If a requirements.yml file is located in the lab directory,
# ansible-galaxy will attempt to install roles and collections
# with the --upgrade option.
#
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
LOG_PATH="${LAB_PREP_FILE_PATH}/logs"

# Python interpreter
PYTHON_VENV=~student/py3venv
PYTHON_BIN=${PYTHON_VENV}/bin/python
PYTHON_PIP_BIN=${PYTHON_VENV}/bin/pip
PYATS_BIN=${PYTHON_VENV}/bin/pyats

# Even though a Python/pyATS binary is explicitly being called from the venv,
# some tools are searching $PATH. Explicitly prepend the path here
PATH=${PYTHON_VENV}/bin:${PATH}

# Set the galaxy bin. Test for presence later, along with a requirements.yml
# file. If both exist, run the installer
ANSIBLE_GALAXY_BIN=${PYTHON_VENV}/bin/ansible-galaxy

# Full path and name of the pyATS testbed and clean file for the lab
PYATS_TESTBED="${TESTBED_PATH}/all_devices.testbed.yml"
PYATS_CLEAN_FILE="${LAB_PREP_FILE_PATH}/prepare_lab.yml"

# Expected lab requirements files for Python and Ansible
LAB_PIP_REQUIREMENTS=${LAB_PREP_FILE_PATH}/requirements.txt
LAB_GALAXY_REQUIREMENTS=${LAB_PREP_FILE_PATH}/requirements.yml

# Generate the commandline
DEVICE_INIT_CMD="${PYATS_BIN} clean \
    --clean-file ${PYATS_CLEAN_FILE} \
    --testbed-file ${PYATS_TESTBED} \
    --no-upload \
    --no-archive \
    --runinfo-dir ${LOG_PATH} \
    --no-mail"

# If a local setup script is present, it will be sourced as the last step.
LOCAL_SETUP_SCRIPT="${LAB_PATH}/localsetup/local_setup.sh"

# Start the lab prep...
echo
echo "******************************************************************************"
echo "Beginning lab preparation tasks..."
echo "******************************************************************************"
echo

echo
echo "******************************************************************************"
echo "Installing additional Python packages..."
echo "******************************************************************************"
echo

# Note: this might result in status != 0 if no requirements are listed.
if [ -e ${LAB_PIP_REQUIREMENTS} ]; then
    ${PYTHON_PIP_BIN} install --upgrade pip setuptools wheel \
        2>&1 > ${LOG_PATH}/pip_lab_install.log.txt

    if [ $? -ne 0 ]; then
        LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
    fi

    ${PYTHON_PIP_BIN} install \
        --upgrade \
        -r ${LAB_PIP_REQUIREMENTS} \
        2>&1 >> ${LOG_PATH}/pip_lab_install.log.txt

    if [ $? -ne 0 ]; then
        LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
    fi
fi

echo
echo "******************************************************************************"
echo "Installing additional Ansible roles and collections..."
echo "******************************************************************************"
echo

# Note: this might result in status != 0 if no requirements are listed.
if [ -x ${ANSIBLE_GALAXY_BIN} ] && [ -f ${LAB_GALAXY_REQUIREMENTS} ]; then
    ${ANSIBLE_GALAXY_BIN} install \
        -r ${LAB_GALAXY_REQUIREMENTS} \
        2>&1 > ${LOG_PATH}/galaxy_repo_install.log.txt

    if [ $? -ne 0 ]; then
        LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
    fi
fi

echo
echo "******************************************************************************"
echo "Configuring devices for the next lab (this will take a few minutes)..."
echo "NOTE: It is safe to ignore 'No clean image provided for device' messages."
echo "******************************************************************************"
echo

if [ -f ${PYATS_CLEAN_FILE} ] && [ -f ${PYATS_TESTBED} ]; then
    # Set the required environment vars and execute the command
    CLEAN_FILE_PATH="${SCRIPT_BASEPATH}/clean_files" \
    DEVICE_CONFIG_PATH="${LAB_PREP_FILE_PATH}/device_configs/pre" \
    ${DEVICE_INIT_CMD} 2>&1 > ${LOG_PATH}/device_init.log.txt

    if [ $? -ne 0 ]; then
        LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
    fi
else
    echo "Unable to initialize devices. Either the pyATS Testbed or the pyATS clean"
    echo "file (prepare_lab.yml) is not present. If this is unexpected, please contact"
    echo "your instructor."

    LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
fi

# If there's a lab-local setup script, source it
if [ -f ${LOCAL_SETUP_SCRIPT} ]; then
    . ${LOCAL_SETUP_SCRIPT}

    if [ $? -ne 0 ]; then
        LAB_INIT_RESULT=$(expr ${LAB_INIT_RESULT} + 1)
    fi

fi

if [ ${LAB_INIT_RESULT} -eq 0 ]; then
    echo
    echo "******************************************************************************"
    echo "SUCCESS! Lab preparation completed"
    echo "******************************************************************************"
    echo
else
    echo
    echo "******************************************************************************"
    echo "ERROR - Lab preparation encontered problems. Please contact your instructor."
    echo "******************************************************************************"
    echo
    exit ${LAB_INIT_RESULT}
fi
