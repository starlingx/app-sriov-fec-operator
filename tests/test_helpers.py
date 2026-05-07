#
# Copyright (c) 2026 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

"""Shared test helper functions for sriov-fec-operator."""

from unittest.mock import MagicMock

from tests import constants as test_const


def create_mock_app(name=None):
    """Create a mock application object.

    Args:
        name: Application name. Defaults to APP_NAME.

    Returns:
        MagicMock with name attribute set.
    """
    mock_app = MagicMock()
    mock_app.name = name or test_const.APP_NAME
    return mock_app


def create_mock_hook_info(
        lifecycle_type, operation, relative_timing,
        extra=None):
    """Create a mock hook_info object for lifecycle tests.

    Args:
        lifecycle_type: The lifecycle type constant.
        operation: The operation constant.
        relative_timing: The timing constant.
        extra: Optional dict for extra hook info data.

    Returns:
        MagicMock configured as hook_info.
    """
    hook_info = MagicMock()
    hook_info.lifecycle_type = lifecycle_type
    hook_info.operation = operation
    hook_info.relative_timing = relative_timing
    if extra is not None:
        hook_info.__contains__ = lambda self, x: x in extra
        hook_info.__getitem__ = lambda self, x: extra[x]
    else:
        hook_info.__contains__ = lambda self, x: False
    return hook_info


def create_mock_dbapi(
        app_id=None, user_overrides=None,
        override_not_found=False):
    """Create a mock dbapi instance.

    Args:
        app_id: The app ID to return from kube_app_get.
        user_overrides: User overrides string.
        override_not_found: If True, helm_override_get raises.

    Returns:
        Configured MagicMock dbapi.
    """
    dbapi = MagicMock()
    mock_kube_app = MagicMock()
    mock_kube_app.id = app_id or test_const.MOCK_DB_APP_ID
    dbapi.kube_app_get.return_value = mock_kube_app

    if override_not_found:
        from sysinv.common import exception
        dbapi.helm_override_get.side_effect = (
            exception.HelmOverrideNotFound(
                name=test_const.HELM_CHART_NAME,
                namespace=test_const.HELM_NS_SRIOV_FEC_SYSTEM
            )
        )
        mock_override = MagicMock()
        mock_override.user_overrides = user_overrides or ""
        dbapi.helm_override_create.return_value = mock_override
    else:
        mock_override = MagicMock()
        mock_override.user_overrides = user_overrides or ""
        dbapi.helm_override_get.return_value = mock_override

    return dbapi


def create_mock_namespace(labels=None):
    """Create a mock Kubernetes namespace object.

    Args:
        labels: Dict of namespace labels.

    Returns:
        MagicMock namespace with metadata.labels.
    """
    namespace = MagicMock()
    namespace.metadata.labels = labels or {}
    return namespace


def create_mock_app_op(dbapi=None, namespace=None):
    """Create a mock AppOperator.

    Args:
        dbapi: Mock dbapi instance.
        namespace: Mock namespace to return from read.

    Returns:
        Configured MagicMock app_op.
    """
    app_op = MagicMock()
    app_op._dbapi = dbapi or create_mock_dbapi()
    client_core = MagicMock()
    if namespace:
        client_core.read_namespace.return_value = namespace
    app_op._kube._get_kubernetesclient_core.return_value = (
        client_core
    )
    app_op._kube.kube_patch_namespace = MagicMock()
    app_op._kube.kube_delete_pod = MagicMock()
    app_op.is_app_aborted.return_value = False
    return app_op
