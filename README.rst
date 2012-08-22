==========================
django-selectable-select2
==========================

.. warning::
    this is still a work in progress

This project is a kind of a plugin for `django-selectable`_.

It provides widgets for use with a great JS library called `select2`_ rather than jQuery UI.
It also provides it's own Lookup classes for better (IMO) serialization results and limiting results (on server side).

.. _django-selectable: https://bitbucket.org/mlavin/django-selectable
.. _select2: http://ivaynberg.github.com/select2/index.html

For now there's only a basic single valued autocomplete widget for usage on ForeignKey (or simply ModelChoiceField) fields.

.. include:: TODO.rst
