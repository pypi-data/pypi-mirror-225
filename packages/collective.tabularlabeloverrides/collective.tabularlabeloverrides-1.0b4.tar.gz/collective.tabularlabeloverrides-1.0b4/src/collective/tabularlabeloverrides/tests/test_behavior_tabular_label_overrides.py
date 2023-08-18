# -*- coding: utf-8 -*-
from collective.tabularlabeloverrides.behaviors.tabular_label_overrides import (
    ITabularLabelOverridesMarker,
)
from collective.tabularlabeloverrides.testing import (  # noqa
    COLLECTIVE_TABULARLABELOVERRIDES_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class TabularLabelOverridesIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_TABULARLABELOVERRIDES_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_tabular_label_overrides(self):
        behavior = getUtility(
            IBehavior, "collective.tabularlabeloverrides.tabular_label_overrides"
        )
        self.assertEqual(
            behavior.marker,
            ITabularLabelOverridesMarker,
        )
