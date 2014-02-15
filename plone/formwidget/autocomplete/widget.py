from AccessControl import getSecurityManager
from AccessControl import ClassSecurityInfo
from Acquisition import Explicit
from Acquisition.interfaces import IAcquirer
from App.class_init import InitializeClass
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import json

import z3c.form.interfaces
import z3c.form.widget
import z3c.form.util
from z3c.formwidget.query.widget import QuerySourceRadioWidget
from z3c.formwidget.query.widget import QuerySourceCheckboxWidget
from zope.interface import implementsOnly, implementer

from plone.formwidget.autocomplete.interfaces import IAutocompleteWidget


class AutocompleteSearch(BrowserView):

    max_results = 10

    def validate_access(self):

        content = self.context.form.context

        # If the object is not wrapped in an acquisition chain
        # we cannot check any permission.
        if not IAcquirer.providedBy(content):
            return

        url = self.request.getURL()
        view_name = url[len(content.absolute_url()):].split('/')[1]

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
            return '[]'

        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        self.context.update()
        source = self.context.bound_source

        # make it unique
        terms = set(source.search(query))

        # sort results and then limit them
        terms = tuple(sorted(terms, key=lambda t: t.title))

        if self.max_results < len(terms):
            terms = terms[:self.max_results]

        return json.dumps([dict(label=t.title or t.token, value=t.token)
                           for t in terms])


class AutocompleteBase(Explicit):
    implementsOnly(IAutocompleteWidget)

    security = ClassSecurityInfo()
    security.declareObjectPublic()

    # XXX: Due to the way the rendering of the QuerySourceRadioWidget works,
    # if we call this 'template' or use a <z3c:widgetTemplate /> directive,
    # we'll get infinite recursion when trying to render the radio buttons.

    input_template = ViewPageTemplateFile('input.pt')
    display_template = None # set by subclass

    # Due to the fact that the widgets inherit from QuerySourceXXXWidget,
    # the klass attribute can't be used without confusing results. This
    # attribute defines the CSS class for the widgets div.
    autocomplete_klass = ''

    # Options passed to jQuery auto-completer
    minLength = 2

    # JavaScript template

    # the funny <" + "input bit is to prevent breakage in testbrowser tests
    # when it parses the js as a real input, but with a bogus value
    # This needs to be a single line string, hence the \ at the end of each line
    js_item_template = """\
    <span id='%(id)s-%(termCount)d-wrapper' class='option'>\
      <" + "input type='radio' id='%(id)s-%(termCount)d' name='%(name)s:list' class='%(klass)s' title='%(title)s' checked='checked' value='" + ui.item.value + "' />\
      <label for='%(id)s-%(termCount)d'>\
        <span class='label'>" + ui.item.label + "</span>\
      </label>\
    </span>\
    """

    js_callback_template = """\
    function(event, ui) {
        var field = $('#%(id)s-input-fields input[value="' + ui.item.value + '"]');
        $('#%(id)s-input-fields input[type=radio]').attr('checked', '');
        if(field.length == 0) {
            $('#%(id)s-%(termCount)d-wrapper').remove();
            $('#%(id)s-input-fields').append(htmlDecode("%(js_item)s"));
        } else {
            field.attr('checked', true);
        }
        $('#%(id)s-widgets-query').attr('value', '');
        event.preventDefault();
    }
    """

    js_template = """\
    function htmlDecode(input){
        return $('<div/>').html(input).html();
    }

    jq(function($) {
        var query_input = $('#%(id)s-widgets-query');
        $('#%(id)s-input-fields').data('klass','%(klass)s').data('title','%(title)s').data('input_type','%(input_type)s');
        $('#%(id)s-buttons-search').remove();
        query_input.autocomplete({
            source: '%(url)s',
            minLength: %(minLength)d,
            select: %(js_callback)s,
            focus: function(event, ui) {
                $('#%(id)s-widgets-query').val(ui.item.label);
                return false;
            }
        });

        var pre_1_9 = query_input.data("autocomplete") ? true : false;
        query_input.data(pre_1_9 ? "autocomplete" : "ui-autocomplete")._renderItem = function(ul, item) {
            return $("<li></li>")
                .data(pre_1_9 ? "item.autocomplete" : "ui-autocomplete-item", item)
                .append("<a>" + item.label + " (" + item.value + ")</a>")
                .appendTo(ul);
        };
        %(js_extra)s
    });
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

        # construct autosearch URL
        form_url = self.request.getURL()
        form_prefix  = z3c.form.util.expandPrefix(self.form.prefix)
        form_prefix += z3c.form.util.expandPrefix(self.__parent__.prefix)
        widget_name = self.name[len(form_prefix):]
        url = "%s/++widget++%s/@@autocomplete-search" % (form_url, widget_name,)

        template_vars = dict(id=self.id,
                             name=self.name,
                             klass=self.klass,
                             title=self.title,
                             termCount=len(self.terms),
                             url=url,
                             minLength=self.minLength,
                             input_type=self.input_type,
                             js_extra=self.js_extra(),
                             )

        template_vars['js_item'] = self.js_item_template % template_vars
        template_vars['js_callback'] = self.js_callback_template % template_vars

        return self.js_template % template_vars


InitializeClass(AutocompleteBase)


class AutocompleteSelectionWidget(AutocompleteBase, QuerySourceRadioWidget):
    """Autocomplete widget that allows single selection.
    """

    autocomplete_klass = u'autocomplete-selection-widget'
    input_type = 'radio'
    display_template = ViewPageTemplateFile('display.pt')


class AutocompleteMultiSelectionWidget(AutocompleteBase,
                                       QuerySourceCheckboxWidget):
    """Autocomplete widget that allows multiple selection
    """

    autocomplete_klass = u'autocomplete-multiselection-widget'
    input_type = 'checkbox'
    display_template = ViewPageTemplateFile('display.pt')

    # the funny <" + "input bit is to prevent breakage in testbrowser tests
    # when it parses the js as a real input, but with a bogus value

    js_item_template = """\
    <span id='%(id)s-" + itemCount + "-wrapper' class='option'>\
      <" + "input type='checkbox' id='%(id)s-" + itemCount + "' name='%(name)s:list' class='%(klass)s' checked='checked' value='" + ui.item.value + "' />\
      <label for='%(id)s-" + itemCount + "'>\
        <span class='label'>" + ui.item.label + "</span>\
      </label>\
    </span>\
    """

    js_callback_template = """\
    function(event, ui) {
        var field = $('#%(id)s-input-fields input[value="' + ui.item.value + '"]');
        if(field.length == 0) {
            var itemCount = $('#%(id)s-input-fields input').length;
            $('#%(id)s-input-fields').append(htmlDecode("%(js_item)s"));
        } else {
            field.attr('checked', true);
        }
        $('#%(id)s-widgets-query').attr('value', '');
        event.preventDefault();
    }
    """

@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        AutocompleteSelectionWidget(request))


@implementer(z3c.form.interfaces.IFieldWidget)
def AutocompleteMultiFieldWidget(field, request):
    return z3c.form.widget.FieldWidget(field,
        AutocompleteMultiSelectionWidget(request))
