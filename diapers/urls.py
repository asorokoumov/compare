__author__ = 'asorokoumov'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^status/$', views.status, name='status'),

    # TODO create human understanding urls
    url(r'^brands/$', views.show_brands, name='brands'),
    url(r'^(?P<brand_id>[0-9]+)/$', views.show_series, name='series'),
    url(r'^(?P<brand_id>[0-9]+)/(?P<series_id>[0-9]+)/$', views.show_sizes, name='sizes'),
    url(r'^(?P<brand_id>[0-9]+)/(?P<series_id>[0-9]+)/(?P<size>.+)/$', views.show_products, name='products'),

    url(r'^parse/recreate/$', views.recreate, name='recreate'),
    url(r'^parse/prices/$', views.update_prices_and_availability, name='update_prices_and_availability'),
    url(r'^parse/manual/$', views.manual_parse, name='manual'),
    url(r'^parse/manual_parse_result/$', views.manual_parse_result, name='manual_parse_result'),
]