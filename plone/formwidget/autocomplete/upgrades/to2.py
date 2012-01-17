from Products.CMFCore.utils import getToolByName


def remove_obsolete_js_and_css(context):
    """Remove JS and CSS files obsolete after the move to jQuery UI
    autocomplete."""

    cssreg = getToolByName(context, 'portal_css')
    cssreg.unregisterResource('++resource++plone.formwidget.autocomplete/jquery.autocomplete.css')

    jsreg = getToolByName(context, 'portal_javascript')
    jsreg.unregisterResource('++resource++plone.formwidget.autocomplete/jquery.autocomplete.min.js')


def enable_jqueryui_plugin(context):
    """Import the registry.xml GS profile to enable the collective.js.jqueryui plugins."""

    gs = getToolByName(context, 'portal_setup')
    profile = 'profile-plone.formwidget.autocomplete:default'
    gs.runImportStepFromProfile(profile, 'registry', purge_old=False)
