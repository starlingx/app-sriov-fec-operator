#
# Copyright (c) 2022-2023 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#
# All Rights Reserved.
#

""" System inventory App lifecycle operator."""

from k8sapp_sriov_fec_operator.common import constants as app_constants
from oslo_log import log as logging
from sysinv.common import constants
from sysinv.common import exception
from sysinv.common import kubernetes
from sysinv.common import utils as cutils
from sysinv.helm import lifecycle_base as base
from sysinv.helm.lifecycle_constants import LifecycleConstants

LOG = logging.getLogger(__name__)


class SriovFecOperatorAppLifecycleOperator(base.AppLifecycleOperator):
    def app_lifecycle_actions(self, context, conductor_obj, app_op, app, hook_info):
        """Perform lifecycle actions for an operation

        :param context: request context, can be None
        :param conductor_obj: conductor object, can be None
        :param app_op: AppOperator object
        :param app: AppOperator.Application object
        :param hook_info: LifecycleHookInfo object

        """
        if hook_info.lifecycle_type == constants.APP_LIFECYCLE_TYPE_FLUXCD_REQUEST:
            if hook_info.operation == constants.APP_APPLY_OP:
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_POST:
                    return self.post_apply(app_op, app, hook_info)

        if hook_info.lifecycle_type == constants.APP_LIFECYCLE_TYPE_OPERATION:
            if hook_info.operation == constants.APP_REMOVE_OP:
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_PRE:
                    return self.pre_remove(app)

        if hook_info.lifecycle_type == constants.APP_LIFECYCLE_TYPE_OPERATION:
            if hook_info.operation == constants.APP_REMOVE_OP:
                if hook_info.relative_timing == constants.APP_LIFECYCLE_TIMING_POST:
                    return self.post_remove(app)

        super(SriovFecOperatorAppLifecycleOperator, self).app_lifecycle_actions(
            context, conductor_obj, app_op, app, hook_info
        )

    def post_apply(self, app_op, app, hook_info):
        if LifecycleConstants.EXTRA not in hook_info:
            raise exception.LifecycleMissingInfo("Missing {}".format(LifecycleConstants.EXTRA))
        if LifecycleConstants.RETURN_CODE not in hook_info[LifecycleConstants.EXTRA]:
            raise exception.LifecycleMissingInfo(
                "Missing {} {}".format(LifecycleConstants.EXTRA, LifecycleConstants.RETURN_CODE))

        # Raise a specific exception to be caught by the
        # retry decorator and attempt a re-apply
        if not hook_info[LifecycleConstants.EXTRA][LifecycleConstants.RETURN_CODE] and \
                not app_op.is_app_aborted(app.name):
            LOG.info("%s app failed applying. Retrying." % str(app.name))
            raise exception.ApplicationApplyFailure(name=app.name)

    def pre_remove(self, app):
        LOG.debug(
            "Executing pre_remove for {} app".format(app_constants.HELM_APP_SRIOV_FEC_OPERATOR)
        )
        LOG.debug("{} app: pre_remove".format(app.name))

    def post_remove(self, app):
        LOG.debug(
            "Executing post_remove for {} app".format(app_constants.HELM_APP_SRIOV_FEC_OPERATOR)
        )
        cmd = ['kubectl', '--kubeconfig', kubernetes.KUBERNETES_ADMIN_CONF,
               'delete', 'namespace', app_constants.HELM_NS_SRIOV_FEC_SYSTEM]
        stdout, stderr = cutils.trycmd(*cmd)
        LOG.debug("{} app: cmd={} stdout={} stderr={}".format(app.name, cmd, stdout, stderr))
