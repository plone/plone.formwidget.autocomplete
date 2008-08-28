from zope.interface import implements, implementer
from zope.component import getMultiAdapter

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.util

from zope.schema.interfaces import ISource, IContextSourceBinder

from z3c.formwidget.query.widget import QuerySourceRadioWidget
from z3c.formwidget.query.widget import QuerySourceCheckboxWidget

from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from AccessControl import getSecurityManager, Unauthorized
from Acquisition import Explicit
from Products.Five.browser import BrowserView

class AutocompleteSearch(BrowserView):
    
    def validate_access(self):
        content = self.context.form.context
        view_name = self.context.form.__name__
        view_instance = getMultiAdapter((content, self.request), name=view_name).__of__(content)
        
        # May raise Unauthorized
        getSecurityManager().validate(content, content, view_name, view_instance)
        
    def __call__(self):
        
        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        self.validate_access()
        
        query = self.request.get('q', None)
        limit = self.request.get('limit', None)
        if not query:
            return ''
        
        source = self.context.source
        
        if IContextSourceBinder.providedBy(source):
            source = source(self.context.context)
        
        assert ISource.providedBy(source)

        # TODO: use limit?
        
        if query:
            terms = set(source.search(query))
        else:
            terms = set()
        
        return '\n'.join(["%s|%s" % (t.token,  t.title or t.token) 
                            for t in sorted(terms, key=lambda t: t.title)])
    
class AutocompleteBase(Explicit):
    implements(IAutocompleteWidget)
    
    # XXX: Due to the way the rendering of the QuerySourceRadioWidget works,
    # if we call this 'template' or use a <z3c:widgetTemplate /> directive,
    # we'll get infinite recursion when trying to render the radio buttons.

    widget_template = ViewPageTemplateFile('autocomplete_input.pt')

    # Options passed to jQuery auto-completer
    autoFill = True
    minChars = 2
    maxResults = 10
    mustMatch = True
    matchContains = True
    multiple = False
    multipleSeparator = ';'
    formatItem = 'function(row, idx, count, value) { return row[1]; }'
    formatResult = 'function(row, idx, count) { return row[0]; }'
    
    def render(self):
        return self.widget_template(self)
    
    def extract(self, default=z3c.form.interfaces.NOVALUE):
        
        subform = self.subform
        search_button_name = subform.buttons['search'].__name__
        search_button_id = z3c.form.util.expandPrefix(subform.prefix) + search_button_name
        
        query_id = subform.widgets['query'].name
        
        if search_button_id in self.request.form:
            # This was a non-AJAX search. The base class will take care of it
            value = self.extractQueryWidget(default)
            
        elif self.name in self.request.form:
            # This was a standard submit and we used the non-AJAX version.
            # Again, let the base class do its thing
            value = self.extractQueryWidget(default)
            
        elif query_id in self.request.form:
            # Form was submitted with a value in the search box and no value
            # for the radio button/checkbox. Thus, the autocomplete widget
            # was used and gave us a value
            
            query_data = subform.widgets['query'].extract()
            tokens = set([token.strip()
                            for token in query_data.split(self.multipleSeparator)
                                if token.strip()])
            
            # Validate the tokens against the original source
            source = self.source

            if IContextSourceBinder.providedBy(source):
                source = source(self.context.context)

            assert ISource.providedBy(source)

            for token in tokens:
                try:
                    term = source.getTermByToken(token)
                except LookupError:
                    return default
            
            value = sorted(tokens)
        else:
            value = default
            
        if value is z3c.form.interfaces.NOVALUE or value is default:
            return value
        elif len(value) == 0:
            return default
        else:
            return value
    
    def js(self):
        
        form_context = self.form.__parent__
        form_name = self.form.__name__
        widget_name = self.name.split('.')[-1]
        
        url = "%s/@@%s/++widget++%s/@@autocomplete-search" % (form_context.absolute_url(), form_name, widget_name)
        
        tokens = [self.terms.getTerm(value).token for value in self.value if value]
        
        return """
        (function($) {
            $().ready(function() {
                $('#%(id)s-buttons-search').remove();
                $('#%(id)s-widgets-query').autocomplete('%(url)s', {
                    autoFill: %(autoFill)s,
                    minChars: %(minChars)d,
                    max: %(maxResults)d,
                    mustMatch: %(mustMatch)s,
                    matchContains: %(matchContains)s,
                    multiple: %(multiple)s,
                    multipleSeparator: '%(multipleSeparator)s',
                    formatItem: %(formatItem)s,
                    formatResult: %(formatResult)s
                });
                $('#%(id)s-widgets-query').attr('value', '%(selected)s');
            });
        })(jQuery);
        """ % dict(url=url,
                   id=self.name.replace('.', '-'), 
                   autoFill=str(self.autoFill).lower(),
                   minChars=self.minChars,
                   maxResults=self.maxResults,
                   mustMatch=str(self.mustMatch).lower(),
                   matchContains=str(self.matchContains).lower(),
                   multiple=str(self.multiple).lower(),
                   multipleSeparator=self.multipleSeparator,
                   formatItem=self.formatItem,
                   formatResult=self.formatResult,
                   selected=self.multipleSeparator.join(tokens))

class AutocompleteSelectionWidget(AutocompleteBase, QuerySourceRadioWidget):
    """Autocomplete widget that allows single selection.
    """
    
class AutocompleteMultiSelectionWidget(AutocompleteBase, QuerySourceCheckboxWidget):
    """Autocomplete widget that allows multiple selection
    """
    
    multiple = True
    
@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, AutocompleteSelectionWidget(request))

@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteMultiFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, AutocompleteMultiSelectionWidget(request))    