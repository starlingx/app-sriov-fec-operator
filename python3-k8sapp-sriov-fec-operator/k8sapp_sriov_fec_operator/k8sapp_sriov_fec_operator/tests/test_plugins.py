#
# Copyright (c) 2022 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_sriov_fec_operator.common import constants as app_constants
from sysinv.tests.helm.test_helm import HelmOperatorTestSuiteMixin

from sysinv.tests.db import base as dbbase


class K8SAppSriovFecOperatorAppMixin(object):
    app_name = app_constants.HELM_APP_SRIOV_FEC_OPERATOR
    path_name = app_name + '.tgz'

    def setUp(self):
        super(K8SAppSriovFecOperatorAppMixin, self).setUp()


# Test Configuration:
# - Controller
# - IPv6
# - Ceph Storage
# - sriov-fec-operator app
class K8SAppSriovFecOperatorControllerTestCase(K8SAppSriovFecOperatorAppMixin,
                                    dbbase.BaseIPv6Mixin,
                                    dbbase.BaseCephStorageBackendMixin,
                                    HelmOperatorTestSuiteMixin,
                                    dbbase.ControllerHostTestCase):
    pass


# Test Configuration:
# - AIO
# - IPv4
# - Ceph Storage
# - sriov-fec-operator-app
class K8SAppSriovFecOperatorAIOTestCase(K8SAppSriovFecOperatorAppMixin,
                             dbbase.BaseCephStorageBackendMixin,
                             HelmOperatorTestSuiteMixin,
                             dbbase.AIOSimplexHostTestCase):
    pass
