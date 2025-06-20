Changelog
=========

1.5.1 (unreleased)
------------------

Breaking changes:

- *add item here*

New features:

- *add item here*

Bug fixes:

- *add item here*


1.5.0 (2025-06-19)
------------------

New features:

- Support proper resource registry settings when installing on Plone 6 as well.  [laulaz]

Bug fixes:

- Minor py3 fixes on the `demo` module. [gforcada]


1.4.1 (2022-04-22)
------------------

Bug fixes:

- Fix ModuleNotFoundError: No module named 'App.class_init' on Plone 6.  [krissik]


1.4.0 (2020-01-27)
------------------

New features:

- Add Plone 5 compatibility
  [laulaz]


1.3.0 (2018-03-07)
------------------

New features:

- Add uninstall profile.
  [thet]


1.2.11 (2016-10-05)
-------------------

Bug fixes:

- Better handling of undefined data
  [agitator]


1.2.10 (2016-08-08)
-------------------

Fixes:

- Update setup.py url to point to github.
  [esteele]

- Use zope.interface decorator.
  [gforcada]

1.2.9 (2016-02-09)
------------------

Fixes:

- Use plone i18n domain
  [staeff]


1.2.8 (2015-04-29)
------------------

* Render CSS as link, no css-import. This allows cooking with other
  link rendered css and gives better asynchronous download behavior.
  [thet]


1.2.7 (2014-10-20)
------------------

* make compatible with jQuery >= 1.9
  [petschki]


1.2.6 (2013-12-07)
------------------

* Fix url in css for indicator.gif
  [mitakas]


1.2.5 (2013-08-23)
------------------

* Use jQuery.prop() instead of jQuery.attr() to deselect radio buttons.
* Only do list marshalling for multiple selection.
* Handle the case where the server responds with 204 No Content.

1.2.4 (2012-10-23)
------------------

* Switch the default parser to use the title as the value, so that titles
  are used to autocomplete what's in the text input box.
  [lentinj]

* Add a custom parse function that defaults to an identical function to the
  default one.
  [lentinj]

1.2.3 (2012-02-13)
------------------

* Fix <input /> element generation for Internet Explorer; in most cases, the
  generated element would be lacking the name attribute.
  [mj]

1.2.2 (2011-09-24)
------------------

* Add whitespace after autocreated radio buttons, fixing alignment:
  http://code.google.com/p/dexterity/issues/detail?id=193 (thanks davidjb)
  [lentinj]

1.2.1 (2011-05-16)
------------------

* Use full widget name in ++widget++ path, don't try and remove form prefix
  (which will not behave correctly if widget is part of a subform).
  [lentinj]

1.2.0 (2011-04-30)
------------------

* Add upgrade step to register formwidget-autocomplete.js, bumping profile
  version to 1
  [lentinj]

* Split input:radio adding function so the code can be reused when adding
  in plone.formwidget.contenttree
  [lentinj]

* Move the javascript callback to real code, so instances of the widget
  can be added to the page by cloning existing widgets
  [lentinj]

* Allow overriding of the autocomplete URL
  [lentinj]

* Fix htmlDecode to return an element, not the nodeValue of an element which
  is null.
  [ggozad]

* No longer include the `demo.zcml` by default, but rather allow users to
  include it if needed.
  [hannosch]

* Update distribution metadata.
  [hannosch]

* Remove direct `zope.app` dependencies.
  [hannosch]

* Use the correct ViewPageTemplateFile from Five required in a Zope 2 context.
  [hannosch]

1.1.1 (2011-02-11)
------------------

* Explicitly include CMFCore's zcml in demo.zcml, for compatibility
  with Zope 2.13.
  [davisagli]

1.1 (2010-08-25)
----------------

* Force the inserted HTML radio buttons to be interpreted as HTML
  instead of text.
  [dukebody]

* Fall back to the site to perform content-related operations if the
  context is not wrapped into an aquisition chain.
  [dukebody]

* Compute the view name as the request URL left-stripped the content
  absolute URL.
  [dukebody]

* Use the same display template for single- and multi-selection:
  The single selection display template was non functional before.
  The value of a single selection field is wrapped in a list anyways
  so the multiselection template renders the single selection field
  just fine.
  -> https://dev.plone.org/plone/ticket/10495

* Update widget in the autocomplete-search browser view:
  The self.context.update() call rebinds to source which previously
  was only bound during traversal. This avoids problems with
  sources that only work after security is applied.
  [gaudenzius]

1.0 - 2010-04-19
----------------

* Issue 107: plone.formwidget.autocomplete: problems in IE8 when changing value
  Added a JavaScript work around, which dechecks all existing radio fields before
  adding a new one which is checked.
  [jbaumann]

* Made the widget work properly in Zope 2.12.
  [optilude]

1.0b3 - 2009-06-29
------------------

* Fix security validator to work properly on add views and other views using
  namespace traversal (++add++...)
  [optilude]

1.0b2 - 2009-04-08
------------------

* Fix security validator to work with urls not including the @@ view name.
  [optilude]

* Made widget use getURL() instead of constructing URL from underlying
  view. This makes it work with complex traversal logic.
  [optilude]

1.0b1 - 2008-08-28
------------------

* Initial release
