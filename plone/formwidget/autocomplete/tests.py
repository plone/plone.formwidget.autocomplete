from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import IntegrationTesting
from zope.configuration import xmlconfig

import doctest
import unittest


class PFAutocompleteLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plone.formwidget.autocomplete

        xmlconfig.file(
            "testing.zcml", plone.formwidget.autocomplete, context=configurationContext
        )


PF_AUTOCOMPLETE_FIXTURE = PFAutocompleteLayer()
PF_AUTOCOMPLETE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PF_AUTOCOMPLETE_FIXTURE,), name="PloneFormWidgetAutocomplete:Integration"
)


def test_suite():
    readme_txt = doctest.DocFileSuite("README.txt")
    readme_txt.layer = PF_AUTOCOMPLETE_INTEGRATION_TESTING
    return unittest.TestSuite(
        [
            readme_txt,
        ]
    )
