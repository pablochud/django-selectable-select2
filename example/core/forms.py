from django import forms
from django.forms.models import modelformset_factory
from django.contrib.localflavor.us.forms import USStateField, USStateSelect

import selectable.forms as selectable

from example.core.lookups import FruitLookup, CityLookup, FancyFruitLookup
from example.core.models import Farm, ReferencesTest
from selectable_select2.widgets import AutoCompleteSelect2Widget as Select2Widget


class ReferencesTestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReferencesTestForm, self).__init__(*args, **kwargs)
        ct = self.fields['city']
        ct.widget = Select2Widget(CityLookup, placeholder="select a state")

    class Meta:
        model = ReferencesTest
        widgets = {
            'fruit2' : Select2Widget(FancyFruitLookup, placeholder='select a fruit')
        }


class ChainedForm(forms.Form):
    city = selectable.AutoComboboxSelectField(
        lookup_class=CityLookup,
        label='City',
        required=False,
    )
    state = USStateField(widget=USStateSelect, required=False)


class FarmForm(forms.ModelForm):

    class Meta(object):
        model = Farm
        widgets = {
            'fruit': selectable.AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
        }


FarmFormset = modelformset_factory(Farm, FarmForm)
