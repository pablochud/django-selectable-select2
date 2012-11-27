from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('example.core.views',
    url(r'^formset/$',              'formset',          name='example-formset'),
    url(r'^advanced/$',             'advanced',         name='example-advanced'),
    url(r'^advanced2/$',            'advanced', {'form_type' : 2},  name='example-advanced'),
    url(r'^listm/$',                'multiple_list',    name='example-multiple-list'),
    url(r'^list/$',                 'list',             name='example-list'),
    url(r'^editm/(?P<pk>\d+)/$',    'multiple_edit',    name='example-multiple'),
    url(r'^edit/(?P<pk>\d+)/$',     'detail',           name='example-detail'),
    url(r'^multiple/$',             'multiple',         name='example-multiple-add'),
    url(r'^$',                      'add',              name='example-index'),
)
