from django import forms
from selectable_select2.widgets import TRANSFERABLE_ATTRS, AutoCompleteSelect2Widget


class Select2ChoiceField(forms.ChoiceField):
    widget = AutoCompleteSelect2Widget

    def __init__(self, lookup_class, *args, **kwargs):
        for attr in TRANSFERABLE_ATTRS:
            setattr(self, attr, kwargs.pop(attr, ''))
        super(Select2ChoiceField, self).__init__(*args, **kwargs)
