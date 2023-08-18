# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.tabularlabeloverrides


class CollectiveTabularlabeloverridesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.tabularlabeloverrides)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.tabularlabeloverrides:default")


COLLECTIVE_TABULARLABELOVERRIDES_FIXTURE = CollectiveTabularlabeloverridesLayer()


COLLECTIVE_TABULARLABELOVERRIDES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TABULARLABELOVERRIDES_FIXTURE,),
    name="CollectiveTabularlabeloverridesLayer:IntegrationTesting",
)


COLLECTIVE_TABULARLABELOVERRIDES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TABULARLABELOVERRIDES_FIXTURE,),
    name="CollectiveTabularlabeloverridesLayer:FunctionalTesting",
)


COLLECTIVE_TABULARLABELOVERRIDES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_TABULARLABELOVERRIDES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveTabularlabeloverridesLayer:AcceptanceTesting",
)
