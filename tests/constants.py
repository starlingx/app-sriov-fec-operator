#
# Copyright (c) 2026 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

"""Shared test constants for sriov-fec-operator tests."""

# Application constants
APP_NAME = 'sriov-fec-operator'
HELM_NS_SRIOV_FEC_SYSTEM = 'sriov-fec-system'
HELM_NS_SRIOV_FEC_OPERATOR = 'sriov-fec-operator'
HELM_CHART_NAME = 'sriov-fec-operator'
COMPONENT_LABEL = 'app.starlingx.io/component'

# Mock database IDs
MOCK_APP_ID = 1
MOCK_DB_APP_ID = 100

# Namespace labels
LABEL_PLATFORM = 'platform'
LABEL_APPLICATION = 'application'

# Override YAML samples
OVERRIDE_PLATFORM_YAML = (
    "app.starlingx.io/component: platform"
)
OVERRIDE_APPLICATION_YAML = (
    "app.starlingx.io/component: application"
)
OVERRIDE_INVALID_YAML = (
    "app.starlingx.io/component: invalid_value"
)
OVERRIDE_EMPTY_YAML = ""
