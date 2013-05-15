from Products.CMFCore.utils import getToolByName

def remoteautocompleteplugin(context):
    """Re-import jsregistry items to pick remove javscript file"""
    gs = getToolByName(context, 'portal_setup')
    profile = 'profile-plone.formwidget.autocomplete:default'
    gs.runImportStepFromProfile(profile, 'jsregistry')
