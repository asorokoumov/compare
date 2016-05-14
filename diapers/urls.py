__author__ = 'asorokoumov'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^status/$', views.status, name='status'),

    url(r'^(?P<brand_id>[0-9]+)/$', views.get_brand, name='brand'),
    url(r'^(?P<brand_id>[0-9]+)/(?P<series_id>[0-9]+)/$', views.get_series, name='series'),

    url(r'^parse/recreate/$', views.recreate, name='recreate'),
    url(r'^parse/prices/$', views.parse_prices, name='parse_prices'),
    url(r'^parse/manual/$', views.manual_parse, name='manual'),
    url(r'^parse/manual_parse_result/$', views.manual_parse_result, name='manual_parse_result'),
]