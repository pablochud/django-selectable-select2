from django import forms
from django.forms.models import modelformset_factory
from django.contrib.localflavor.us.forms import USStateSelect  # , USStateField

import selectable.forms as selectable

from example.core.lookups import FruitLookup, CityLookup, CityChainedLookup, FancyFruitLookup, StateLookup
from example.core.models import Farm, ReferencesTest  # , City
from selectable_select2.widgets import AutoCompleteSelect2Widget as Select2Widget
# from selectable_select2.forms import Select2DependencyFormMixin
from selectable_select2.forms import Select2DependencyForm
from django.contrib.localflavor.us.us_states import STATE_CHOICES


class ReferencesTestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReferencesTestForm, self).__init__(*args, **kwargs)
        ct = self.fields['city']
        ct.widget = Select2Widget(CityLookup, placeholder="select a city", limit=20)

    class Meta:
        model = ReferencesTest
        widgets = {
            'fruit2' : Select2Widget(FancyFruitLookup, placeholder='select a fruit')
        }


class ChainedForm(forms.Form):
    state = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
        #USStateField(
            widget=Select2Widget(StateLookup, placeholder="select a state"),
            #widget=USStateSelect,
            required=False)

    state2 = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
        #USStateField(
            #widget=Select2Widget(StateLookup, placeholder="select a state"),
            widget=USStateSelect,
            required=False)

    # city = selectable.AutoComboboxSelectField(lookup_class=CityChainedLookup, label='City', required=False, )
    city = forms.ModelChoiceField(empty_label= "", queryset=CityChainedLookup().get_queryset(),
        widget=Select2Widget(
            CityChainedLookup,
            placeholder="select a city",
            parents="id_state,id_state2",
            clearonparentchange=True))


class ChainedForm2(Select2DependencyForm):
    state = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
        #USStateField(
            widget=Select2Widget(StateLookup, placeholder="select a state"),
            #widget=USStateSelect,
            required=False)
    state2 = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
        #USStateField(
            #widget=Select2Widget(StateLookup, placeholder="select a state"),
            widget=USStateSelect,
            required=False)

    # city = selectable.AutoComboboxSelectField(lookup_class=CityChainedLookup, label='City', required=False, )
    city = forms.ModelChoiceField(empty_label= "", queryset=CityChainedLookup().get_queryset(),
        widget=Select2Widget(CityChainedLookup, placeholder="select a city"))

    select2_deps = (
        ('city', { 'parents' : ['state', 'state2'] } ),
     )


class FarmForm(forms.ModelForm):

    class Meta(object):
        model = Farm
        widgets = {
            'fruit': selectable.AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
        }


FarmFormset = modelformset_factory(Farm, FarmForm)
