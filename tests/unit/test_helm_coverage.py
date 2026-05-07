#
# Copyright (c) 2026 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for sriov_fec_operator helm module."""

import unittest

from tests import constants as test_const


class TestSriovFecOperatorHelmBasic(unittest.TestCase):
    """Test SriovFecOperatorHelm basic functionality."""

    def setUp(self):
        """Set up test fixtures."""
        from k8sapp_sriov_fec_operator.helm import sriov_fec_operator as helm_mod
        self.helm_mod = helm_mod
        self.helm_class = helm_mod.SriovFecOperatorHelm

    def test_chart_constant(self):
        """Verify CHART matches expected chart name."""
        self.assertEqual(
            self.helm_class.CHART,
            test_const.HELM_CHART_NAME
        )

    def test_service_name_constant(self):
        """Verify SERVICE_NAME matches expected app name."""
        self.assertEqual(
            self.helm_class.SERVICE_NAME,
            test_const.APP_NAME
        )

    def test_supported_namespaces_contains_system(self):
        """Verify SUPPORTED_NAMESPACES includes fec-system."""
        self.assertIn(
            test_const.HELM_NS_SRIOV_FEC_SYSTEM,
            self.helm_class.SUPPORTED_NAMESPACES
        )

    def test_supported_app_namespaces_key(self):
        """Verify SUPPORTED_APP_NAMESPACES has app key."""
        self.assertIn(
            test_const.APP_NAME,
            self.helm_class.SUPPORTED_APP_NAMESPACES
        )

    def test_supported_app_namespaces_value(self):
        """Verify app namespaces include fec-system."""
        ns_list = self.helm_class.SUPPORTED_APP_NAMESPACES[
            test_const.APP_NAME
        ]
        self.assertIn(
            test_const.HELM_NS_SRIOV_FEC_SYSTEM, ns_list
        )


class TestSriovFecOperatorHelmMethods(unittest.TestCase):
    """Test SriovFecOperatorHelm instance methods."""

    def setUp(self):
        """Set up helm instance with mocked parent."""
        from k8sapp_sriov_fec_operator.helm import sriov_fec_operator as helm_mod
        self.helm_class = helm_mod.SriovFecOperatorHelm
        self.instance = object.__new__(self.helm_class)

    def test_get_namespaces_returns_list(self):
        """Verify get_namespaces returns a list."""
        result = self.instance.get_namespaces()
        self.assertIsInstance(result, list)

    def test_get_namespaces_contains_system_ns(self):
        """Verify get_namespaces includes fec-system ns."""
        result = self.instance.get_namespaces()
        self.assertIn(
            test_const.HELM_NS_SRIOV_FEC_SYSTEM, result
        )

    def test_get_overrides_valid_namespace(self):
        """Test get_overrides with valid namespace."""
        result = self.instance.get_overrides(
            namespace=test_const.HELM_NS_SRIOV_FEC_SYSTEM
        )
        self.assertIsInstance(result, dict)

    def test_get_overrides_no_namespace(self):
        """Test get_overrides with no namespace returns all."""
        result = self.instance.get_overrides(namespace=None)
        self.assertIsInstance(result, dict)
        self.assertIn(
            test_const.HELM_NS_SRIOV_FEC_SYSTEM, result
        )

    def test_get_overrides_invalid_namespace_raises(self):
        """Test get_overrides with invalid namespace raises."""
        from sysinv.common.exception import InvalidHelmNamespace
        with self.assertRaises(InvalidHelmNamespace):
            self.instance.get_overrides(
                namespace='invalid-namespace'
            )

    def test_get_overrides_empty_string_namespace(self):
        """Test get_overrides with empty string namespace."""
        result = self.instance.get_overrides(namespace='')
        self.assertIsInstance(result, dict)


class TestSriovFecOperatorHelmConstants(unittest.TestCase):
    """Test the constants module directly."""

    def test_helm_app_name(self):
        """Verify HELM_APP_SRIOV_FEC_OPERATOR value."""
        from k8sapp_sriov_fec_operator.common import constants as app_const
        self.assertEqual(
            app_const.HELM_APP_SRIOV_FEC_OPERATOR,
            'sriov-fec-operator'
        )

    def test_helm_ns_system(self):
        """Verify HELM_NS_SRIOV_FEC_SYSTEM value."""
        from k8sapp_sriov_fec_operator.common import constants as app_const
        self.assertEqual(
            app_const.HELM_NS_SRIOV_FEC_SYSTEM,
            'sriov-fec-system'
        )

    def test_helm_ns_operator(self):
        """Verify HELM_NS_SRIOV_FEC_OPERATOR value."""
        from k8sapp_sriov_fec_operator.common import constants as app_const
        self.assertEqual(
            app_const.HELM_NS_SRIOV_FEC_OPERATOR,
            'sriov-fec-operator'
        )

    def test_helm_chart_name(self):
        """Verify HELM_CHART_SRIOV_FEC_OPERATOR value."""
        from k8sapp_sriov_fec_operator.common import constants as app_const
        self.assertEqual(
            app_const.HELM_CHART_SRIOV_FEC_OPERATOR,
            'sriov-fec-operator'
        )

    def test_component_label(self):
        """Verify HELM_COMPONENT_LABEL value."""
        from k8sapp_sriov_fec_operator.common import constants as app_const
        self.assertEqual(
            app_const.HELM_COMPONENT_LABEL_SRIOV_FEC_OPERATOR,
            'app.starlingx.io/component'
        )


if __name__ == '__main__':
    unittest.main()
