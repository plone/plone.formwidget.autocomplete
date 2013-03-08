from zope import component
from zope import interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder

from z3c.formwidget.query.interfaces import IQuerySource
from z3c.form.interfaces import IFieldsForm
from z3c.form import form, field, button

from Products.Five import BrowserView

from plone.autoform.form import AutoExtensibleForm
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.z3cform.layout import wrap_form


class ItalianCities(object):
    interface.implements(IQuerySource)

    vocabulary = SimpleVocabulary((
        SimpleTerm(u'Bologna', 'bologna', u'Bologna'),
        SimpleTerm(u'Palermo', 'palermo', u'Palermo'),
        SimpleTerm(u'Sorrento', 'sorrento', u'Sorrento'),
        SimpleTerm(u'Torino', 'torino', u'Torino')))

    def __init__(self, context):
        self.context = context

    __contains__ = vocabulary.__contains__
    __iter__ = vocabulary.__iter__
    getTerm = vocabulary.getTerm
    getTermByToken = vocabulary.getTermByToken

    def search(self, query_string):
        return [v for v in self if query_string.lower() in v.value.lower()]


class ItalianCitiesSourceBinder(object):
    interface.implements(IContextSourceBinder)

    def __call__(self, context):
        return ItalianCities(context)


class ICities(interface.Interface):
    favourite_city = schema.Choice(title=u"Favourite city",
                                   source=ItalianCitiesSourceBinder())
    visited_cities = schema.List(
        title=u"Visited cities",
        value_type=schema.Choice(title=u"Selection",
                                 source=ItalianCitiesSourceBinder()))


class CitiesForm(form.Form):
    interface.implements(ICities)
    fields = field.Fields(ICities)
    fields['favourite_city'].widgetFactory = AutocompleteFieldWidget
    fields['visited_cities'].widgetFactory = AutocompleteMultiFieldWidget

    @button.buttonAndHandler(u'Apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        print "Submitted data:", data

form_view = wrap_form(CitiesForm)


class CitiesFormAdapter(object):
    component.adapts(interface.Interface)
    interface.implements(ICities)

    def __init__(self, context):
        self.context = context
        self.visited_cities = None
        self.favourite_city = None
