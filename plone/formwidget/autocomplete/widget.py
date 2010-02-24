from zope.interface import implements, implementsOnly, implementer

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.util

from z3c.formwidget.query.widget import QuerySourceRadioWidget
from z3c.formwidget.query.widget import QuerySourceCheckboxWidget

from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from AccessControl import getSecurityManager
from Acquisition import Explicit
from Products.Five.browser import BrowserView

class AutocompleteSearch(BrowserView):
    
    def validate_access(self):
        
        content = self.context.form.context
        view_name = self.request.getURL().split('/')[-3] # /path/to/obj/++widget++wname/@@autocomplete-search?q=foo

        # May raise Unauthorized
        
        # If the view is 'edit', then traversal prefers the view and
        # restrictedTraverse prefers the edit() method present on most CMF
        # content. Sigh...
        if not view_name.startswith('@@') and not view_name.startswith('++'):
            view_name = '@@' + view_name
        
        view_instance = content.restrictedTraverse(view_name)
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
        
        source = self.context.bound_source

        # TODO: use limit?
        
        if query:
            terms = set(source.search(query))
        else:
            terms = set()
        
        return '\n'.join(["%s|%s" % (t.token,  t.title or t.token) 
                            for t in sorted(terms, key=lambda t: t.title)])
    
class AutocompleteBase(Explicit):
    implementsOnly(IAutocompleteWidget)
    
    # XXX: Due to the way the rendering of the QuerySourceRadioWidget works,
    # if we call this 'template' or use a <z3c:widgetTemplate /> directive,
    # we'll get infinite recursion when trying to render the radio buttons.

    input_template = ViewPageTemplateFile('input.pt')
    display_template = None # set by subclass
    
    # Options passed to jQuery auto-completer
    autoFill = True
    minChars = 2
    maxResults = 10
    mustMatch = True
    matchContains = True
    formatItem = 'function(row, idx, count, value) { return row[1]; }'
    formatResult = 'function(row, idx, count) { return ""; }'
    
    # JavaScript template
    
    # the funny <" + "input bit is to prevent breakage in testbrowser tests
    # when it parses the js as a real input, but with a bogus value
    js_callback_template = """\
    function(event, data, formatted) {
        var field = $('#%(id)s-input-fields input[value="' + data[0] + '"]');
        $('#%(id)s-input-fields input[type=radio]').attr('checked', '');
        if(field.length == 0) {
            $('#%(id)s-%(termCount)d-wrapper').remove();
            $('#%(id)s-input-fields').append("<span id='%(id)s-%(termCount)d-wrapper' class='option'><" + "input type='radio' id='%(id)s-%(termCount)d' name='%(name)s:list' class='%(klass)s' title='%(title)s' checked='checked' value='" + data[0] + "' /><label for='%(id)s-%(termCount)d'><span class='label'>" + data[1] + "</span></label></span>");
        } else {
            field.each(function() { this.checked = true });
        }
        $('#%(id)s-widgets-query').each(function() { this.value = "" });
    }
    """
    
    js_template = """\
    (function($) {
        $().ready(function() {
            $('#%(id)s-buttons-search').remove();
            $('#%(id)s-widgets-query').autocomplete('%(url)s', {
                autoFill: %(autoFill)s,
                minChars: %(minChars)d,
                max: %(maxResults)d,
                mustMatch: %(mustMatch)s,
                matchContains: %(matchContains)s,
                formatItem: %(formatItem)s,
                formatResult: %(formatResult)s
            }).result(%(js_callback)s);
            %(js_extra)s
        });
    })(jQuery);
    """
    
    # Override this to insert additional JavaScript
    def js_extra(self):
        return ""
    
    def render(self):
        if self.mode == z3c.form.interfaces.DISPLAY_MODE:
            return self.display_template(self)
        else:
            return self.input_template(self)
    
    def js(self):
        
        form_url = self.request.getURL()
        
        form_prefix = self.form.prefix + self.__parent__.prefix
        widget_name = self.name[len(form_prefix):]
        
        url = "%s/++widget++%s/@@autocomplete-search" % (form_url, widget_name,)

        js_callback = self.js_callback_template % dict(id=self.id,
                                                       name=self.name,
                                                       klass=self.klass,
                                                       title=self.title,
                                                       termCount=len(self.terms))
        
        return self.js_template % dict(id=self.id,
                                       url=url,
                                       autoFill=str(self.autoFill).lower(),
                                       minChars=self.minChars,
                                       maxResults=self.maxResults,
                                       mustMatch=str(self.mustMatch).lower(),
                                       matchContains=str(self.matchContains).lower(),
                                       formatItem=self.formatItem,
                                       formatResult=self.formatResult,
                                       js_callback=js_callback,
                                       js_extra=self.js_extra())

class AutocompleteSelectionWidget(AutocompleteBase, QuerySourceRadioWidget):
    """Autocomplete widget that allows single selection.
    """
    
    klass = u'autocomplete-selection-widget'
    display_template = ViewPageTemplateFile('display_selection.pt')
    
class AutocompleteMultiSelectionWidget(AutocompleteBase, QuerySourceCheckboxWidget):
    """Autocomplete widget that allows multiple selection
    """
    
    klass = u'autocomplete-multiselection-widget'
    display_template = ViewPageTemplateFile('display_multiselection.pt')
    
    # the funny <" + "input bit is to prevent breakage in testbrowser tests
    # when it parses the js as a real input, but with a bogus value
    js_callback_template = """\
    function(event, data, formatted) {
        var field = $('#%(id)s-input-fields input[value="' + data[0] + '"]');
        if(field.length == 0) {
            var itemCount = $('#%(id)s-input-fields input').length;
            $('#%(id)s-input-fields').append("<span id='%(id)s-" + itemCount + "-wrapper' class='option'><" + "input type='checkbox' id='%(id)s-" + itemCount + "' name='%(name)s:list' class='%(klass)s' checked='checked' value='" + data[0] + "' /><label for='%(id)s-" + itemCount + "'><span class='label'>" + data[1] + "</span></label></span>");
        } else {
            field.each(function() { this.checked = true });
        }
    }
    """
    
@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, AutocompleteSelectionWidget(request))

@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteMultiFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field, AutocompleteMultiSelectionWidget(request))
