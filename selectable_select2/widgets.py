#from selectable.forms.widgets import AutoCompleteWidget
from django.conf import settings
from django import forms
from django.utils import simplejson as json
from django.utils.http import urlencode
from collections import Iterable


__all__ = ('AutoCompleteSelect2Widget',)

MEDIA_URL = settings.MEDIA_URL
STATIC_URL = getattr(settings, 'STATIC_URL', u'')
MEDIA_PREFIX = u'{0}selectable_select2/'.format(STATIC_URL or MEDIA_URL)

# these are the kwargs that u can pass when instantiating the widget
TRANSFERABLE_ATTRS = ('placeholder', 'parent_ids', 'clearonparentchange', 'parent_namemap')

# a subset of TRANSFERABLE_ATTRS that should be serialized on "data-djsels2-*" attrs
SERIALIZABLE_ATTRS = ('clearonparentchange',)

# a subset of TRANSFERABLE_ATTRS that should be also on "data-*" attrs
EXPLICIT_TRANSFERABLE_ATTRS = ('placeholder',)

ARRAY_TRANSFERABLE_ATTRS = ('initialselection',)

ALL_TRANSFERABLE_ATTRS = TRANSFERABLE_ATTRS + ARRAY_TRANSFERABLE_ATTRS


class SelectableSelect2MediaMixin(object):

    class Media(object):
        css = {
            'all': (u'{0}css/select2.css'.format(MEDIA_PREFIX),)
        }
        js = (
            u'{0}js/jquery.django.admin.fix.js'.format(MEDIA_PREFIX),
            u'{0}js/select2.min.js'.format(MEDIA_PREFIX),
            u'{0}js/jquery.dj.selectable.select2.js'.format(MEDIA_PREFIX),
        )


class AutoCompleteWidget(SelectableSelect2MediaMixin):

    selectable_type = "select2"

    def __init__(self, lookup_class, *args, **kwargs):
        self.lookup_class = lookup_class
        self.allow_new = kwargs.pop('allow_new', False)
        self.qs = kwargs.pop('query_params', {})
        self.limit = kwargs.pop('limit', None)

        for attr in ALL_TRANSFERABLE_ATTRS:
            setattr(self, attr, kwargs.pop(attr, ''))

        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def update_query_parameters(self, qs_dict):
        self.qs.update(qs_dict)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(AutoCompleteWidget, self).build_attrs(extra_attrs, **kwargs)
        url = self.lookup_class.url()
        if self.limit and 'limit' not in self.qs:
            self.qs['limit'] = self.limit
        if self.qs:
            url = '%s?%s' % (url, urlencode(self.qs))
        attrs[u'data-selectable-url'] = url
        attrs[u'data-selectable-type'] = self.selectable_type
        attrs[u'data-selectable-allow-new'] = str(self.allow_new).lower()

        new_attrs = self.custom_build_attrs()
        attrs.update(new_attrs)
        return attrs

    def custom_build_attrs(self):
        attrs = {}

        for real_attr in TRANSFERABLE_ATTRS:
            attr = real_attr.replace('_', '-')
            value = getattr(self, real_attr)

            # because django widget can't properly output json in his attrs
            # so we're flattening the map into string of comma delimitted strings
            # in form "key0,value0,key1,value1,..."
            if real_attr == 'parent_namemap':
                if isinstance(value, dict):
                    value_copy = value.copy()
                    value = []
                    for k, v in value_copy.items():
                        value.extend([k, v])
                value = ",".join(value)

            if real_attr in SERIALIZABLE_ATTRS:
                value = json.dumps(value)
            attrs[u'data-djsels2-' + attr] = value
            if real_attr in EXPLICIT_TRANSFERABLE_ATTRS:
                attrs[u'data-' + attr] = value

        for real_attr in ARRAY_TRANSFERABLE_ATTRS:
            attr = real_attr.replace('_', '-')
            value_list = getattr(self, real_attr)

            for index, value in enumerate(value_list):
                attrs[u'data-djsels2-' + attr + "-no" + str(index)] = value

        attrs[u'data-selectable-type'] = self.selectable_type

        return attrs


class Select2BaseWidget(AutoCompleteWidget):

    def render(self, name, value, attrs=None):
        # when there is a value and no initialselection was passed to the widget
        if value is not None and (self.initialselection is None or self.initialselection == ''):
            lookup = self.lookup_class()
            if not isinstance(value, Iterable):
                new_value = [value]
            else:
                new_value = value
            selections = []
            for val in new_value:
                item = lookup.get_item(val)
                if item is not None:
                    initialselection = lookup.get_item_value(item)
                    selections.append(initialselection)
            self.initialselection = selections

        return super(Select2BaseWidget, self).render(name, value, attrs)


class AutoCompleteSelect2Widget(Select2BaseWidget, forms.TextInput):
    pass


#class AutoCompleteMultipleSelect2Widget(Select2BaseWidget, BaseAutoCompleteWidget, forms.MultipleHiddenInput):

from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
# from itertools import
from django.utils.datastructures import MultiValueDict, MergeDict


class SelectMultipleSelectedOnly(forms.TextInput):
    allow_multiple_selected = True

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_unicode(v) for v in selected_choices if v != ',')
        # output = []

        lookup = self.lookup_class()
        options_values = []
        options_labels = []

        for _pk in selected_choices:
            options_values.append(_pk)
            item = lookup.get_item(_pk)
            if item is not None:
                selection = lookup.get_item_value(item)
            options_labels.append(selection)

        self.initialselection = options_labels

        # for option_value, option_label in options:

        #     if isinstance(option_label, (list, tuple)):
        #         output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
        #         for option in option_label:
        #             output.append(self.render_option(selected_choices, *option))
        #         output.append(u'</optgroup>')
        #     else:
        #         output.append(self.render_option(selected_choices, option_value, option_label))
        return u', '.join(options_values)

    def render(self, name, value, attrs=None, choices=()):
        print "V", value
        if value is None:
            value = ''
        options = self.render_options(choices, value)
        final_attrs = self.build_attrs(attrs, name=name, type='text')
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(options)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

    def value_from_datadict(self, data, files, name):
        print "DATA", data, type(data), files, name
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    # def _has_changed(self, initial, data):
    #     if initial is None:
    #         initial = []
    #     if data is None:
    #         data = []
    #     if len(initial) != len(data):
    #         return True
    #     initial_set = set([force_unicode(value) for value in initial])
    #     data_set = set([force_unicode(value) for value in data])
    #     return data_set != initial_set

# TODO: zrobic tak by to byly dwa widgety (normalny input i jakies multiple-hidden) i nasluchiwac na eventy zmiany i dodania

class AutoCompleteMultipleSelect2Widget(AutoCompleteWidget, SelectMultipleSelectedOnly):
# class AutoCompleteMultipleSelect2Widget(AutoCompleteWidget, forms.SelectMultiple):

    selectable_type = "selectx2_multiple"

    # def render(self, *args, **kwargs):
    #     print args, kwargs, "render"
    #     return super(AutoCompleteMultipleSelect2Widget, self).render(*args, **kwargs)

    # def value_from_datadict(self, data, files, name):
    #     print data, type(data), "data"
    #     return super(AutoCompleteMultipleSelect2Widget, self).value_from_datadict(data, files, name)
