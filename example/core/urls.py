from django.conf.urls import patterns, url


urlpatterns = patterns('core.views',
    url(r'^formset/$',   'formset',  name='example-formset'),
    url(r'^advanced/$',  'advanced', name='example-advanced'),
    url(r'^advanced2/$', 'advanced', {'form_type' : 2},  name='example-advanced'),
    url(r'^list/$',      'list',     name='example-list'),
    url(r'^edit/(?P<pk>\d+)$',     'detail',     name='example-detail'),
    url(r'^$',           'add',      name='example-index'),
)
