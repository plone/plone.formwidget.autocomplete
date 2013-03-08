from Products.CMFCore.utils import getToolByName
PROFILEID = 'profile-plone.formwidget.autocomplete:default'


def common(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile(PROFILEID)
