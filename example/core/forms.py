from django import forms
from django.forms.models import modelformset_factory
from localflavor.us.forms import USStateSelect  # , USStateField
from localflavor.us.us_states import STATE_CHOICES

import selectable.forms as selectable

from .lookups import FruitLookup, CityLookup, CityChainedLookup, FancyFruitLookup, StateLookup
from .models import Farm, ReferencesTest  # , City
from selectable_select2.widgets import AutoCompleteSelect2Widget as Select2Widget
# from selectable_select2.forms import Select2DependencyFormMixin
from selectable_select2.forms import Select2DependencyForm


class ReferencesTestForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReferencesTestForm, self).__init__(*args, **kwargs)
        ct = self.fields['city']
        ct.widget = Select2Widget(CityLookup, placeholder="select a city", limit=20)

    class Meta:
        model = ReferencesTest
        fields = ('city', 'fruit', 'fruit2', 'farm')
        widgets = {
            'fruit2' : Select2Widget(FancyFruitLookup, placeholder='select a fruit')
        }


class ChainedForm(forms.Form):
    state = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
                              widget=Select2Widget(StateLookup, placeholder="select a state"),
                              required=False)

    state2 = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
                               widget=USStateSelect,
                               required=False)

    # city = selectable.AutoComboboxSelectField(lookup_class=CityChainedLookup, label='City', required=False, )
    city = forms.ModelChoiceField(empty_label= "", queryset=CityChainedLookup().get_queryset(),
                                    widget=Select2Widget(  # noqa
                                        CityChainedLookup,
                                        placeholder = "select a city",
                                        parent_ids = "id_state,id_state2",
                                        clearonparentchange = True,
                                        parent_namemap = {'id_state' : 'state', 'id_state2' : 'state' }
                                        )
                                    )


class ChainedForm2(Select2DependencyForm):
    state = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
                              widget=Select2Widget(StateLookup, placeholder="select a state"),
                              required=False)

    state2 = forms.ChoiceField(choices = (('', '---'),) + STATE_CHOICES,
                               widget=USStateSelect,
                               required=False)

    # city = selectable.AutoComboboxSelectField(lookup_class=CityChainedLookup, label='City', required=False, )
    city = forms.ModelChoiceField(empty_label= "", queryset=CityChainedLookup().get_queryset(),
                                  widget=Select2Widget(CityChainedLookup, placeholder="select a city"))

    select2_deps = (
        ('city', {
            'parents' : ['state', 'state2'],
            'parents_namemap' : { 'state2' : 'state' },
        }),
    )


class FarmForm(forms.ModelForm):

    class Meta(object):
        model = Farm
        fields = ('name', 'owner', 'fruit')
        widgets = {
            'fruit': selectable.AutoCompleteSelectMultipleWidget(lookup_class=FruitLookup),
        }


FarmFormset = modelformset_factory(Farm, FarmForm)
