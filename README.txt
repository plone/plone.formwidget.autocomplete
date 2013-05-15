Introduction
============

plone.formwidget.autocomplete is a z3c.form widget for use with Plone. It
uses the jQuery Autocomplete widget, and has graceful fallback for non-
Javascript browsers.

There is a single-select version (AutocompleteFieldWidget) for
Choice fields, and a multi-select one (AutocompleteMultiFieldWidget)
for collection fields (e.g. List, Tuple) with a value_type of Choice.

When using this widget, the vocabulary/source has to provide the IQuerySource
interface from z3c.formwidget.query and have a search() method.

Customization
-------------
Previously, customization of the javascript options was done by setting
options on the widgets. That is still possible for minLength. For any other
customizations the only way to customize the autocomplete works be deactivating the autocomplete for the given widget and then writing your own initalization code. The initalization code is quite simple, so please don't feel intimidated by it.
Deactivation of the autocomplete functionality happens by setting the
triggerAutocomplete Attribute on the widget to something falsy.

