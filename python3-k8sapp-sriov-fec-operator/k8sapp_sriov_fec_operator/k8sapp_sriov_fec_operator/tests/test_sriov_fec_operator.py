# Copyright (c) 2022-2024 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_sriov_fec_operator.tests import test_plugins

from sysinv.tests.db import base as dbbase
from sysinv.db import api as dbapi
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base


class SriovFecOperatorTestCase(test_plugins.K8SAppSriovFecOperatorAppMixin,
                    base.HelmTestCaseMixin):

    def setUp(self):
        super(SriovFecOperatorTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='sriov-fec-operator')
        self.dbapi = dbapi.get_instance()


class SriovFecOperatorTestCaseDummy(SriovFecOperatorTestCase, dbbase.ProvisionedControllerHostTestCase):
    # without a test zuul will fail
    def test_dummy(self):
        pass
