from django.contrib.auth.models import User

# from selectable_select2.base import ModelLookup, LookupBase
from selectable.base import ModelLookup, LookupBase
from selectable.registry import registry

from .models import Fruit, City
from django import template

from localflavor.us.us_states import STATE_CHOICES


class FruitLookup(ModelLookup):
    model = Fruit
    search_fields = ('name__icontains', )

registry.register(FruitLookup)


class FancyFruitLookup(FruitLookup):

    def get_item_label(self, item):
        tpl = """
        <table class="selectable_table">
            <tr>
                <td rowspan="2" class="image">
                    <img src="{{ item.fruit_image.url }}" alt="" width="50px" height="50px">
                </td>
                <td>{{ item.name }}</td>
            </tr>
            <tr>
                <td class="small">{{ item.desc }}</td>
            </tr>
        </table>"""
        tpl = template.Template(tpl)
        return tpl.render(template.Context({ 'item' : item }))

    # def get_item_value(self, item):
    #     pass  # we use a default implementation of `get_item_value`

registry.register(FancyFruitLookup)


class OwnerLookup(ModelLookup):
    model = User
    search_fields = ('username__icontains', )

registry.register(OwnerLookup)


class CityChainedLookup(ModelLookup):
    model = City
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(CityChainedLookup, self).get_query(request, term)
        state = request.GET.get('state', '')

        # support for second field
        if state == '':
            state = request.GET.get('state2', '')

        if state:
            results = results.filter(state=state)
        else:
            results = []
        return results

    def get_item_label(self, item):
        return u"{0}, {1}".format(item.name, item.state)


class CityLookup(ModelLookup):
    model = City
    search_fields = ('name__icontains', )

    def get_item_label(self, item):
        return u"{0}, {1}".format(item.name, item.state)


registry.register(CityLookup)
registry.register(CityChainedLookup)


class StateLookup(LookupBase):

    def get_query(self, request, term):
        choices = STATE_CHOICES[:]

        def filter_function(item):
            if not term or term.lower() in item[1].lower():
                return True
            return False
        return filter(filter_function, choices)

    def get_item_id(self, item):
        return item[0]

    def get_item_label(self, item):
        return item[1]

    def get_item_value(self, item):
        return item[1]

registry.register(StateLookup)
