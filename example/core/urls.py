from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('example.core.views',
    url(r'^formset/',  'formset',  name='example-formset'),
    url(r'^advanced/', 'advanced', name='example-advanced'),
    url(r'^list/',     'list',     name='example-list'),
    url(r'^',          'add',      name='example-index'),
)
