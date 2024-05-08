#
# Copyright (c) 2022-2024 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception
from sysinv.helm import base

from k8sapp_sriov_fec_operator.common import constants as app_constants


class SriovFecOperatorHelm(base.BaseHelm):
    """Class to encapsulate helm operations for the Sriov fec operator chart"""

    SUPPORTED_NAMESPACES = base.BaseHelm.SUPPORTED_NAMESPACES + \
        [app_constants.HELM_NS_SRIOV_FEC_SYSTEM]
    SUPPORTED_APP_NAMESPACES = {
        app_constants.HELM_APP_SRIOV_FEC_OPERATOR:
            base.BaseHelm.SUPPORTED_NAMESPACES +
            [app_constants.HELM_NS_SRIOV_FEC_SYSTEM],
    }

    CHART = app_constants.HELM_CHART_SRIOV_FEC_OPERATOR

    SERVICE_NAME = app_constants.HELM_APP_SRIOV_FEC_OPERATOR

    def get_namespaces(self):
        return self.SUPPORTED_NAMESPACES

    def get_overrides(self, namespace=None):
        overrides = {
            app_constants.HELM_NS_SRIOV_FEC_SYSTEM: {}
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
