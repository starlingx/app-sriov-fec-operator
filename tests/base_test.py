#
# Copyright (c) 2026 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

"""Base test class for sriov-fec-operator unit tests."""

import unittest

from tests import constants as test_const
from tests import test_helpers as helpers


class BaseSriovFecTestCase(unittest.TestCase):
    """Base test case with common setUp for module tests.

    Provides mock app, app_op, dbapi, and namespace objects
    pre-configured for sriov-fec-operator testing.
    """

    def setUp(self):
        """Set up test fixtures common to all tests."""
        self.mock_app = helpers.create_mock_app()
        self.mock_namespace = helpers.create_mock_namespace(
            labels={test_const.COMPONENT_LABEL: 'platform'}
        )
        self.mock_dbapi = helpers.create_mock_dbapi()
        self.mock_app_op = helpers.create_mock_app_op(
            dbapi=self.mock_dbapi,
            namespace=self.mock_namespace
        )
