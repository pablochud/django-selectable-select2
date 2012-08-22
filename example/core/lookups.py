from django.contrib.auth.models import User

from selectable_select2.base import ModelLookup
from selectable.registry import registry

from example.core.models import Fruit, City
from django import template


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


class CityLookup(ModelLookup):
    model = City
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(CityLookup, self).get_query(request, term)
        state = request.GET.get('state', '')
        if state:
            results = results.filter(state=state)
        return results

    def get_item_label(self, item):
        return u"%s, %s" % (item.name, item.state)

registry.register(CityLookup)
