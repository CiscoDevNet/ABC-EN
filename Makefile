##########################################################################
# Traverse all lab paths and process Makefiles to generate lab
# initialization configs for each.
#
# Usage:
#     make configs
#
# LAB NAME: ABC-EN
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

# Find all lab_prep_files directories inside each lab path
SUBDIRS := $(wildcard */lab_prep_files/)

# Process each SUBDIR and, if a Makefile is present, make the configs.
.PHONY: configs $(SUBDIRS)
configs: $(SUBDIRS)
$(SUBDIRS):
	@if [ -f "$@/Makefile" ]; then \
  		$(MAKE) -C $@ ; \
  	fi
