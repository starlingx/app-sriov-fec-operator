#
# Copyright (c) 2026 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

"""Unit tests for lifecycle_sriov_fec_operator module."""

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from tests import constants as test_const
from tests import test_helpers as helpers
from tests.base_test import BaseSriovFecTestCase


class TestLifecycleActions(BaseSriovFecTestCase):
    """Test app_lifecycle_actions dispatch logic."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.lc_mod = lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    def test_post_apply_dispatch(self):
        """Test lifecycle dispatches to post_apply."""
        from sysinv.helm.lifecycle_constants import LifecycleConstants
        from sysinv.common import constants as sys_const

        hook_info = helpers.create_mock_hook_info(
            lifecycle_type=(
                LifecycleConstants.APP_LIFECYCLE_TYPE_FLUXCD_REQUEST
            ),
            operation=sys_const.APP_APPLY_OP,
            relative_timing=(
                LifecycleConstants.APP_LIFECYCLE_TIMING_POST
            ),
            extra={
                LifecycleConstants.EXTRA: {
                    LifecycleConstants.RETURN_CODE: True
                }
            },
        )
        # app_lifecycle_actions should not raise an exception
        with patch.object(
            self.operator, 'post_apply'
        ) as mock_post:
            self.operator.app_lifecycle_actions(
                None, None, self.mock_app_op,
                self.mock_app, hook_info
            )
            mock_post.assert_called_once()

    def test_pre_remove_dispatch(self):
        """Test lifecycle dispatches to pre_remove."""
        from sysinv.helm.lifecycle_constants import LifecycleConstants
        from sysinv.common import constants as sys_const

        hook_info = helpers.create_mock_hook_info(
            lifecycle_type=(
                LifecycleConstants.APP_LIFECYCLE_TYPE_OPERATION
            ),
            operation=sys_const.APP_REMOVE_OP,
            relative_timing=(
                LifecycleConstants.APP_LIFECYCLE_TIMING_PRE
            ),
        )
        with patch.object(
            self.operator, 'pre_remove'
        ) as mock_pre:
            self.operator.app_lifecycle_actions(
                None, None, self.mock_app_op,
                self.mock_app, hook_info
            )
            mock_pre.assert_called_once()

    def test_post_remove_dispatch(self):
        """Test lifecycle dispatches to post_remove."""
        from sysinv.helm.lifecycle_constants import LifecycleConstants
        from sysinv.common import constants as sys_const

        hook_info = helpers.create_mock_hook_info(
            lifecycle_type=(
                LifecycleConstants.APP_LIFECYCLE_TYPE_OPERATION
            ),
            operation=sys_const.APP_REMOVE_OP,
            relative_timing=(
                LifecycleConstants.APP_LIFECYCLE_TIMING_POST
            ),
        )
        with patch.object(
            self.operator, 'post_remove'
        ) as mock_post:
            self.operator.app_lifecycle_actions(
                None, None, self.mock_app_op,
                self.mock_app, hook_info
            )
            mock_post.assert_called_once()

    def test_unhandled_lifecycle_calls_super(self):
        """Test unhandled lifecycle type calls super."""
        hook_info = helpers.create_mock_hook_info(
            lifecycle_type='unknown_type',
            operation='unknown_op',
            relative_timing='unknown_timing',
        )
        # Unhandled lifecycle type should not raise; delegates to super()
        self.operator.app_lifecycle_actions(
            None, None, self.mock_app_op,
            self.mock_app, hook_info
        )


class TestPostApply(BaseSriovFecTestCase):
    """Test post_apply method branches."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    def _make_hook_info(self, return_code=True):
        """Create hook_info with EXTRA and RETURN_CODE.

        Args:
            return_code: The return code value.

        Returns:
            Configured hook_info mock.
        """
        from sysinv.helm.lifecycle_constants import LifecycleConstants
        extra_data = {
            LifecycleConstants.RETURN_CODE: return_code
        }
        hook_info = MagicMock()
        hook_info.__contains__ = (
            lambda self, x: x == LifecycleConstants.EXTRA
        )
        hook_info.__getitem__ = (
            lambda self, x: extra_data
            if x == LifecycleConstants.EXTRA
            else None
        )
        return hook_info

    def test_post_apply_missing_extra_raises(self):
        """Test post_apply raises when EXTRA missing."""
        from sysinv.common.exception import LifecycleMissingInfo

        hook_info = MagicMock()
        hook_info.__contains__ = lambda self, x: False

        with self.assertRaises(LifecycleMissingInfo):
            self.operator.post_apply(
                self.mock_app_op, self.mock_app, hook_info
            )

    def test_post_apply_missing_return_code_raises(self):
        """Test post_apply raises when RETURN_CODE missing."""
        from sysinv.common.exception import LifecycleMissingInfo
        from sysinv.helm.lifecycle_constants import LifecycleConstants

        hook_info = MagicMock()
        hook_info.__contains__ = (
            lambda self, x: x == LifecycleConstants.EXTRA
        )
        hook_info.__getitem__ = lambda self, x: {}

        with self.assertRaises(LifecycleMissingInfo):
            self.operator.post_apply(
                self.mock_app_op, self.mock_app, hook_info
            )

    def test_post_apply_failed_retries(self):
        """Test post_apply raises retry on failure."""
        from sysinv.common.exception import ApplicationApplyFailure

        hook_info = self._make_hook_info(return_code=False)
        self.mock_app_op.is_app_aborted.return_value = False

        with self.assertRaises(ApplicationApplyFailure):
            self.operator.post_apply(
                self.mock_app_op, self.mock_app, hook_info
            )

    def test_post_apply_aborted_no_retry(self):
        """Test post_apply does not retry if aborted."""
        hook_info = self._make_hook_info(return_code=False)
        self.mock_app_op.is_app_aborted.return_value = True

        # Should not raise ApplicationApplyFailure
        self.operator.post_apply(
            self.mock_app_op, self.mock_app, hook_info
        )

    def test_post_apply_success_platform_label(self):
        """Test post_apply sets platform label by default."""
        hook_info = self._make_hook_info(return_code=True)

        # No user overrides - defaults to platform
        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(user_overrides="")
        )

        self.operator.post_apply(
            self.mock_app_op, self.mock_app, hook_info
        )
        # Verify namespace was patched
        self.mock_app_op._kube.kube_patch_namespace\
            .assert_called()

    def test_post_apply_application_override(self):
        """Test post_apply with application override."""
        hook_info = self._make_hook_info(return_code=True)

        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(
                user_overrides=(
                    test_const.OVERRIDE_APPLICATION_YAML
                )
            )
        )

        self.operator.post_apply(
            self.mock_app_op, self.mock_app, hook_info
        )
        self.mock_app_op._kube.kube_patch_namespace\
            .assert_called()

    def test_post_apply_platform_override(self):
        """Test post_apply with platform override."""
        hook_info = self._make_hook_info(return_code=True)

        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(
                user_overrides=(
                    test_const.OVERRIDE_PLATFORM_YAML
                )
            )
        )

        self.operator.post_apply(
            self.mock_app_op, self.mock_app, hook_info
        )
        self.mock_app_op._kube.kube_patch_namespace\
            .assert_called()

    def test_post_apply_invalid_override_logs_warning(self):
        """Test post_apply with unsupported override value."""
        hook_info = self._make_hook_info(return_code=True)

        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(
                user_overrides=(
                    test_const.OVERRIDE_INVALID_YAML
                )
            )
        )

        # Invalid YAML override should not raise an exception, just logs a warning
        self.operator.post_apply(
            self.mock_app_op, self.mock_app, hook_info
        )


class TestPostApplyLabelChange(BaseSriovFecTestCase):
    """Test post_apply namespace label change logic."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    def _make_hook_info(self):
        """Create successful hook_info."""
        from sysinv.helm.lifecycle_constants import LifecycleConstants
        extra_data = {
            LifecycleConstants.RETURN_CODE: True
        }
        hook_info = MagicMock()
        hook_info.__contains__ = (
            lambda self, x: x == LifecycleConstants.EXTRA
        )
        hook_info.__getitem__ = (
            lambda self, x: extra_data
        )
        return hook_info

    def test_label_change_triggers_pod_delete(self):
        """Test label change deletes pods."""
        hook_info = self._make_hook_info()

        # Old label is 'application', new will be 'platform'
        self.mock_namespace.metadata.labels = {
            test_const.COMPONENT_LABEL: 'application'
        }
        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(user_overrides="")
        )

        with patch.object(
            self.operator,
            '_delete_security_profiles_operator_pods'
        ) as mock_del:
            self.operator.post_apply(
                self.mock_app_op, self.mock_app, hook_info
            )
            mock_del.assert_called_once()

    def test_same_label_no_pod_delete(self):
        """Test same label does not delete pods."""
        hook_info = self._make_hook_info()

        # Old label is already 'platform'
        self.mock_namespace.metadata.labels = {
            test_const.COMPONENT_LABEL: 'platform'
        }
        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(user_overrides="")
        )

        with patch.object(
            self.operator,
            '_delete_security_profiles_operator_pods'
        ) as mock_del:
            self.operator.post_apply(
                self.mock_app_op, self.mock_app, hook_info
            )
            mock_del.assert_not_called()


class TestPreRemove(BaseSriovFecTestCase):
    """Test pre_remove method."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    def test_pre_remove_does_not_raise(self):
        """Test pre_remove executes without error."""
        self.operator.pre_remove(self.mock_app)

    def test_pre_remove_with_custom_app_name(self):
        """Test pre_remove with custom app name."""
        custom_app = helpers.create_mock_app(name='custom')
        self.operator.pre_remove(custom_app)


class TestPostRemove(BaseSriovFecTestCase):
    """Test post_remove method."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    @patch('k8sapp_sriov_fec_operator.lifecycle'
           '.lifecycle_sriov_fec_operator.cutils.trycmd')
    def test_post_remove_calls_kubectl_delete(
            self, mock_trycmd):
        """Test post_remove calls kubectl delete ns."""
        mock_trycmd.return_value = ('', '')
        self.operator.post_remove(self.mock_app)
        mock_trycmd.assert_called_once()

    @patch('k8sapp_sriov_fec_operator.lifecycle'
           '.lifecycle_sriov_fec_operator.cutils.trycmd')
    def test_post_remove_cmd_includes_namespace(
            self, mock_trycmd):
        """Test post_remove command includes correct ns."""
        mock_trycmd.return_value = ('deleted', '')
        self.operator.post_remove(self.mock_app)
        call_args = mock_trycmd.call_args
        # Verify namespace is in the command
        args = call_args[0] if call_args[0] else []
        self.assertIn(
            test_const.HELM_NS_SRIOV_FEC_SYSTEM, args
        )


class TestGetHelmUserOverrides(BaseSriovFecTestCase):
    """Test _get_helm_user_overrides method."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    def test_returns_user_overrides(self):
        """Test returns user_overrides string."""
        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(user_overrides="test: value")
        )
        result = self.operator._get_helm_user_overrides(
            self.mock_dbapi, test_const.MOCK_DB_APP_ID
        )
        self.assertEqual(result, "test: value")

    def test_returns_empty_when_no_overrides(self):
        """Test returns empty string when no overrides."""
        self.mock_dbapi.helm_override_get.return_value = (
            MagicMock(user_overrides=None)
        )
        result = self.operator._get_helm_user_overrides(
            self.mock_dbapi, test_const.MOCK_DB_APP_ID
        )
        self.assertEqual(result, "")

    def test_creates_override_when_not_found(self):
        """Test creates override when HelmOverrideNotFound."""
        from sysinv.common.exception import HelmOverrideNotFound
        self.mock_dbapi.helm_override_get.side_effect = (
            HelmOverrideNotFound(
                name=test_const.HELM_CHART_NAME,
                namespace=test_const.HELM_NS_SRIOV_FEC_SYSTEM
            )
        )
        mock_created = MagicMock(user_overrides="")
        self.mock_dbapi.helm_override_create.return_value = (
            mock_created
        )

        result = self.operator._get_helm_user_overrides(
            self.mock_dbapi, test_const.MOCK_DB_APP_ID
        )
        self.assertEqual(result, "")
        self.mock_dbapi.helm_override_create.assert_called_once()


class TestDeleteSecurityProfilesPods(BaseSriovFecTestCase):
    """Test _delete_security_profiles_operator_pods."""

    def setUp(self):
        """Set up lifecycle operator instance."""
        super().setUp()
        from k8sapp_sriov_fec_operator.lifecycle import lifecycle_sriov_fec_operator as lc_mod
        self.operator = lc_mod.SriovFecOperatorAppLifecycleOperator()

    @patch('k8sapp_sriov_fec_operator.lifecycle'
           '.lifecycle_sriov_fec_operator.cutils.trycmd')
    def test_deletes_lease(self, mock_trycmd):
        """Test deletes the lease resource."""
        mock_trycmd.return_value = ('', '')
        client_core = MagicMock()
        mock_pod = MagicMock()
        mock_pod.metadata.name = 'test-pod'
        client_core.list_namespaced_pod.return_value = (
            MagicMock(items=[mock_pod])
        )

        self.operator._delete_security_profiles_operator_pods(
            self.mock_app_op, client_core
        )
        mock_trycmd.assert_called_once()

    @patch('k8sapp_sriov_fec_operator.lifecycle'
           '.lifecycle_sriov_fec_operator.cutils.trycmd')
    def test_deletes_pods(self, mock_trycmd):
        """Test deletes all pods in namespace."""
        mock_trycmd.return_value = ('', '')
        client_core = MagicMock()
        mock_pod1 = MagicMock()
        mock_pod1.metadata.name = 'pod-1'
        mock_pod2 = MagicMock()
        mock_pod2.metadata.name = 'pod-2'
        client_core.list_namespaced_pod.return_value = (
            MagicMock(items=[mock_pod1, mock_pod2])
        )

        self.operator._delete_security_profiles_operator_pods(
            self.mock_app_op, client_core
        )
        self.assertEqual(
            self.mock_app_op._kube.kube_delete_pod.call_count,
            2
        )

    @patch('k8sapp_sriov_fec_operator.lifecycle'
           '.lifecycle_sriov_fec_operator.cutils.trycmd')
    def test_no_pods_no_delete(self, mock_trycmd):
        """Test no pods means no delete calls."""
        mock_trycmd.return_value = ('', '')
        client_core = MagicMock()
        client_core.list_namespaced_pod.return_value = (
            MagicMock(items=[])
        )

        self.operator._delete_security_profiles_operator_pods(
            self.mock_app_op, client_core
        )
        self.mock_app_op._kube.kube_delete_pod\
            .assert_not_called()


if __name__ == '__main__':
    unittest.main()
