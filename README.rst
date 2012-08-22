==========================
django-selectable-select2
==========================

.. warning::
    this is still a work in progress

This project is a kind of a plugin for `django-selectable`_.

It provides widgets for use with a great JS library called `select2`_ rather than jQuery UI.
It also provides it's own Lookup classes for better (IMO) serialization results and limiting results (on server side).

For now there's only a basic single valued autocomplete widget for usage on ForeignKey (or simply ModelChoiceField) fields.

Installation and usage
=========================

* install `django-selectable`_ (you can ommit the part regarding jquery-ui)

* add `selectable_select2` to `INSTALLED_APPS`. So it look like this::

    INSTALLED_APPS = (
        ...
        'selectable',
        'selectable_select2',
        ...
    )

* define your `lookup class`_

.. note::
    as for now (until `issue #64`_ is resolved) you should inherit from ``selectable_select2.base.LookupBase`` and ``selectable_select2.base.ModelLookup``

* in your forms you can use ``selectable_select2.widgets.AutoCompleteSelect2Widget`` like so::

    from selectable_select2.widgets import AutoCompleteSelect2Widget
    from django import forms

    from myapp.models import MyModel  # example model with a ForeignKey called ``myfk``
    from myapp.lookups import MyModelLookup  # the lookup defined in previous step

    class MyModelForm(forms.ModelForm):

        class Meta:
            model = MyModel
            widgets = {
                'myfk' : AutoCompleteSelect2Widget(MyModelLookup, placeholder='select related item')
            }


Check the `example` project for more details.


.. include:: TODO.rst

.. _issue #64: https://bitbucket.org/mlavin/django-selectable/issue/64/decouple-building-results-from
.. _django-selectable: https://bitbucket.org/mlavin/django-selectable
.. _select2: http://ivaynberg.github.com/select2/index.html
.. _lookup class: http://django-selectable.readthedocs.org/en/latest/lookups.html
