from Products.CMFCore.utils import getToolByName


def upgrade(context):
    """Upgrade to v2"""
    # Import migration profile
    gs = getToolByName(context, 'portal_setup')
    profile = 'profile-plone.formwidget.autocomplete.upgrades:to_v2'
    gs.runAllImportStepsFromProfile(profile, purge_old=False)
