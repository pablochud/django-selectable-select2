from django import forms
from django.forms.models import modelformset_factory
from django.contrib.localflavor.us.forms import USStateField, USStateSelect

import selectable.forms as selectable

from example.core.lookups import FruitLookup, CityLookup, FancyFruitLookup
from example.core.models import Farm, ReferencesTest
from selectable_select2.widgets import AutoCompleteSelect2Widget as Select2Widget


class FruitForm(forms.Form):

    dummy   = forms.CharField(required=True)

    select2 = forms.CharField(
        label = 'Select2 test',
        widget = Select2Widget(FruitLookup, placeholder="select a fruit"),
        required = False,
    )

    city = forms.CharField(
        label='City test',
        widget = Select2Widget(CityLookup, placeholder="select a state"),
        required = False
    )

    select2fancy = forms.CharField(
        label='Select2 fancy test',
        widget=Select2Widget(FancyFruitLookup, attrs={'class' : 'input-xxlarge'}),
        required=False,
    )


class ReferencesTestForm(forms.ModelForm):
    # city = forms.CharField(
    #     label='City test',
    #     widget = Select2Widget(CityLookup, placeholder="select a state"),
    #     # required = False
    # )

    def __init__(self, *args, **kwargs):
        super(ReferencesTestForm, self).__init__(*args, **kwargs)
        ct = self.fields['city']
        obj = None
        if self.instance.pk is not None:
            obj = self.instance.city
        init_sel = ct.label_from_instance(obj)
        ct.widget = Select2Widget(CityLookup, placeholder="select a state", initial_selection = init_sel)

    class Meta:
        model = ReferencesTest

    '''
    autocomplete = forms.CharField(
        label='Type the name of a fruit (AutoCompleteWidget)',
        widget=selectable.AutoCompleteWidget(FruitLookup),
        required=False,
    )
    newautocomplete = forms.CharField(
        label='Type the name of a fruit (AutoCompleteWidget which allows new items)',
        widget=selectable.AutoCompleteWidget(FruitLookup, allow_new=True),
        required=False,
    )
    combobox = forms.CharField(
        label='Type/select the name of a fruit (AutoComboboxWidget)',
        widget=selectable.AutoComboboxWidget(FruitLookup),
        required=False,
    )
    newcombobox = forms.CharField(
        label='Type/select the name of a fruit (AutoComboboxWidget which allows new items)',
        widget=selectable.AutoComboboxWidget(FruitLookup, allow_new=True),
        required=False,
    )
    # AutoCompleteSelectField (no new items)
    autocompleteselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteField)',
        required=False,
    )
    # AutoCompleteSelectField (allows new items)
    newautocompleteselect = selectable.AutoCompleteSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoCompleteField which allows new items)',
        required=False,
    )
    # AutoComboboxSelectField (no new items)
    comboboxselect = selectable.AutoComboboxSelectField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoComboboxSelectField)',
        required=False,
    )
    # AutoComboboxSelectField (allows new items)
    newcomboboxselect = selectable.AutoComboboxSelectField(
        lookup_class=FruitLookup,
        allow_new=True,
        label='Select a fruit (AutoComboboxSelectField which allows new items)',
        required=False,
    )
    # AutoCompleteSelectMultipleField
    multiautocompleteselect = selectable.AutoCompleteSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoCompleteSelectMultipleField)',
        required=False,
    )
    # AutoComboboxSelectMultipleField
    multicomboboxselect = selectable.AutoComboboxSelectMultipleField(
        lookup_class=FruitLookup,
        label='Select a fruit (AutoComboboxSelectMultipleField)',
        required=False,
    )
    '''


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
