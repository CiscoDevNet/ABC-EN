##########################################################################
# Create device configs for lab initialization from prerequisite labs.
# LAB NAME: ABC-EN/python
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

##########################################################################
# CHANGE AS NEEDED:
# Define prerequisite labs, in the order of execution. Each line is a
# relative path to the lab source in this repo.
#
LAB_PREREQUISITES := \
        ../../ansible_playbooks \
        ../../pyats_testing \
        ../../pyats_config \
        ../../mdp \
        ../../insomnia

##########################################################################
# Lines below should not need to be changed!
#
# Configs for this lab will be saved in this location
TARGET_PATH := ./device_configs/pre

# Wildcard path - search all prerequisite dirs for this target path
CONFIG_FILE_PATH := lab_prep_files/device_configs/post

# All devices associated with ABC-EN-A
DEVICES :=        \
	provider-rtr1 \
	inet-rtr1     \
	inet-rtr2     \
	core-rtr3     \
	core-rtr4     \
	access-rtr5   \
	access-rtr6   \

.PHONY: configs $(DEVICES)
configs: $(DEVICES)
$(DEVICES):
	@echo
	@echo "***********************************************************************"
	@echo "* Generating pre-lab configuration file for device '$@'"
	@echo "***********************************************************************"

# Remove the existing targets
	@rm -f ${TARGET_PATH}/$@.cfg.txt

# Process each pre-req and append to the destination file
	@for CONFIG_PATH in $(LAB_PREREQUISITES); do \
  		if [ -f "$${CONFIG_PATH}/$(CONFIG_FILE_PATH)/$@.cfg.txt" ] ; then \
  			cat $${CONFIG_PATH}/$(CONFIG_FILE_PATH)/$@.cfg.txt >> ${TARGET_PATH}/$@.cfg.txt ; \
		fi ; \
	 done
