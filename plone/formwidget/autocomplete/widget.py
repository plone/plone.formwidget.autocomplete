from urllib import unquote
from json import dumps

from AccessControl import getSecurityManager
from AccessControl import ClassSecurityInfo
from Acquisition import Explicit
from Acquisition.interfaces import IAcquirer
from App.class_init import InitializeClass
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import z3c.form.interfaces
import z3c.form.widget
import z3c.form.util
from z3c.formwidget.query.widget import QuerySourceRadioWidget
from z3c.formwidget.query.widget import QuerySourceCheckboxWidget
from zope.interface import implementsOnly, implementer

from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget


class AutocompleteSearch(BrowserView):

    def validate_access(self):

        content = self.context.form.context

        # If the object is not wrapped in an acquisition chain
        # we cannot check any permission.
        if not IAcquirer.providedBy(content):
            return

        url = self.request.getURL()
        view_name = unquote(url[len(content.absolute_url()):].split('/')[1])

        # May raise Unauthorized

        # If the view is 'edit', then traversal prefers the view and
        # restrictedTraverse prefers the edit() method present on most CMF
        # content. Sigh...
        if not view_name.startswith('@@') and not view_name.startswith('++'):
            view_name = '@@' + view_name

        view_instance = content.restrictedTraverse(view_name)
        sm = getSecurityManager()
        sm.validate(content, content, view_name, view_instance)

    def __call__(self):

        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()

        query = self.request.get('term', None)
        if not query:
            return ''

        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        self.context.update()
        source = self.context.bound_source
        # TODO: use limit?

        if query:
            terms = set(source.search(query))
        else:
            terms = set()

        retval = []
        for term in sorted(terms, key=lambda t: t.title):
            retval.append(dict(label=term.title or term.token,
                value=term.token))
        return dumps(retval)


class AutocompleteBase(Explicit):
    implementsOnly(IAutocompleteWidget)

    security = ClassSecurityInfo()
    security.declareObjectPublic()

    # XXX: Due to the way the rendering of the QuerySourceRadioWidget works,
    # if we call this 'template' or use a <z3c:widgetTemplate /> directive,
    # we'll get infinite recursion when trying to render the radio buttons.

    input_template = ViewPageTemplateFile('input.pt')
    display_template = None  # set by subclass

    # Options passed to jQuery auto-completer
    minLength = 2

    # Override if you want to customize autocomplete even further
    triggerAutocomplete = True
    js = ""

    def render(self):
        if self.mode == z3c.form.interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)

    def css_class_for_autocomplete_initalization(self):
        if self.triggerAutocomplete:
            return "pfa_autocomplete"
        else:
            return ""

    def autocomplete_url(self):
        """Generate the URL that returns autocomplete results for this form
        """
        form_url = self.request.getURL()

        return "%s/++widget++%s/@@autocomplete-search" % (
            form_url, self.name)


InitializeClass(AutocompleteBase)


class AutocompleteSelectionWidget(AutocompleteBase, QuerySourceRadioWidget):
    """Autocomplete widget that allows single selection.
    """

    klass = u'autocomplete-selection-widget'
    input_type = 'radio'
    display_template = ViewPageTemplateFile('display.pt')


class AutocompleteMultiSelectionWidget(AutocompleteBase,
                                       QuerySourceCheckboxWidget):
    """Autocomplete widget that allows multiple selection
    """

    klass = u'autocomplete-multiselection-widget'
    input_type = 'checkbox'
    multiple = True
    display_template = ViewPageTemplateFile('display.pt')


@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        AutocompleteSelectionWidget(request))


@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteMultiFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        AutocompleteMultiSelectionWidget(request))
