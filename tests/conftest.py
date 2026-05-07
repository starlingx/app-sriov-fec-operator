#
# Copyright (c) 2026 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

"""Pytest configuration and fixtures for sriov-fec-operator."""

import os
import sys
import types
from unittest.mock import MagicMock

# Ensure project source is importable
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
K8SAPP_ROOT = os.path.join(
    PROJECT_ROOT,
    'python3-k8sapp-sriov-fec-operator',
    'k8sapp_sriov_fec_operator'
)
if K8SAPP_ROOT not in sys.path:
    sys.path.insert(0, K8SAPP_ROOT)


def _make_module(name, attrs=None):
    """Create a fake module with given attributes.

    Args:
        name: Module name.
        attrs: Dict of attributes to set.

    Returns:
        A types.ModuleType instance.
    """
    mod = types.ModuleType(name)
    if attrs:
        for key, val in attrs.items():
            setattr(mod, key, val)
    return mod


# --- Exception classes ---

class InvalidHelmNamespace(Exception):
    """Mock InvalidHelmNamespace exception."""

    def __init__(self, chart=None, namespace=None):
        """Initialize with chart and namespace."""
        super().__init__(
            f"Invalid namespace {namespace} for {chart}"
        )


class LifecycleMissingInfo(Exception):
    """Mock LifecycleMissingInfo exception."""
    pass


class ApplicationApplyFailure(Exception):
    """Mock ApplicationApplyFailure exception."""

    def __init__(self, name=None):
        """Initialize with app name."""
        super().__init__(f"App {name} apply failure")


class HelmOverrideNotFound(Exception):
    """Mock HelmOverrideNotFound exception."""

    def __init__(self, name=None, namespace=None):
        """Initialize with name and namespace."""
        super().__init__(f"Not found: {name}/{namespace}")


# --- Base classes ---

class BaseHelm:
    """Mock BaseHelm class."""

    SUPPORTED_NAMESPACES = ['kube-system']

    def __init__(self):
        """Initialize BaseHelm."""
        pass


class AppLifecycleOperator:
    """Mock AppLifecycleOperator base class."""

    def app_lifecycle_actions(
            self, context, conductor_obj, app_op, app,
            hook_info):
        """Default lifecycle actions (no-op)."""
        pass


class LifecycleConstants:
    """Mock LifecycleConstants."""

    APP_LIFECYCLE_TYPE_FLUXCD_REQUEST = 'fluxcd-request'
    APP_LIFECYCLE_TYPE_OPERATION = 'operation'
    APP_LIFECYCLE_TIMING_POST = 'post'
    APP_LIFECYCLE_TIMING_PRE = 'pre'
    EXTRA = 'extra'
    RETURN_CODE = 'return_code'


# --- Register modules ---

mock_logger = MagicMock()

MODULES = {
    'sysinv': _make_module('sysinv'),
    'sysinv.common': _make_module('sysinv.common'),
    'sysinv.common.exception': _make_module(
        'sysinv.common.exception', {
            'InvalidHelmNamespace': InvalidHelmNamespace,
            'LifecycleMissingInfo': LifecycleMissingInfo,
            'ApplicationApplyFailure': ApplicationApplyFailure,
            'HelmOverrideNotFound': HelmOverrideNotFound,
        }),
    'sysinv.common.constants': _make_module(
        'sysinv.common.constants', {
            'APP_APPLY_OP': 'apply',
            'APP_REMOVE_OP': 'remove',
        }),
    'sysinv.common.kubernetes': _make_module(
        'sysinv.common.kubernetes', {
            'KUBERNETES_ADMIN_CONF': '/etc/kubernetes/admin.conf',
        }),
    'sysinv.common.utils': _make_module(
        'sysinv.common.utils', {
            'trycmd': MagicMock(return_value=('', '')),
        }),
    'sysinv.helm': _make_module('sysinv.helm'),
    'sysinv.helm.base': _make_module(
        'sysinv.helm.base', {
            'BaseHelm': BaseHelm,
        }),
    'sysinv.helm.lifecycle_base': _make_module(
        'sysinv.helm.lifecycle_base', {
            'AppLifecycleOperator': AppLifecycleOperator,
        }),
    'sysinv.helm.lifecycle_constants': _make_module(
        'sysinv.helm.lifecycle_constants', {
            'LifecycleConstants': LifecycleConstants,
        }),
    'sysinv.db': _make_module('sysinv.db'),
    'sysinv.db.api': _make_module('sysinv.db.api'),
    'oslo_log': _make_module('oslo_log', {
        'log': _make_module('oslo_log.log', {
            'getLogger': MagicMock(return_value=mock_logger),
        }),
    }),
    'oslo_log.log': None,  # Set below
}

# oslo_log.log references the sub-module
MODULES['oslo_log.log'] = _make_module('oslo_log.log', {
    'getLogger': MagicMock(return_value=mock_logger),
})

for mod_name, mod_obj in MODULES.items():
    if mod_obj is not None:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = mod_obj
