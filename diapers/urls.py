__author__ = 'asorokoumov'
from django.conf.urls import url

from . import views
from views import *

urlpatterns = [

    url(r'^admin/$', views.admin, name='admin'),

    # admin
    url(r'^parse/parse_shop_catalog/$', views.parse_shop_catalog, name='parse_shop_catalog'),
    url(r'^parse/update_brand_list/$', views.update_brand_list, name='update_brand_list'),
    url(r'^parse/recreate/$', views.recreate, name='recreate'),
    url(r'^parse/prices/$', views.update_prices_and_availability, name='update_prices_and_availability'),
    url(r'^parse/manual/$', views.manual_parse, name='manual'),
    url(r'^parse/manual_parse_result/$', views.manual_parse_result, name='manual_parse_result'),


    #  New design
    url(r'^$', views.index, name='index'),
    url(r'^podguzniki/$', views.redirect_to_index, name='redirect_to_index'),


    url(r'^get_series/(?P<brand_id>[-\w]+)/', views.get_series, name='get_series'),
    url(r'^get_brands/(?P<brand_id>[-\w]+)/(?P<series_id>[-\w]+)/', views.get_brands, name='get_brand'),
    url(r'^get_sizes/(?P<brand_id>[-\w]+)/(?P<series_id>[-\w]+)/', views.get_sizes, name='get_sizes'),

    url(r'^search/$', views.search, name='search'),
    url(r'^podguzniki/(?P<brand>[-\w ]+)/(?P<series>[-\w ]+)/(?P<size>[-\w]+)/$', views.products, name='products'),
    url(r'^podguzniki/(?P<brand>[-\w ]+)/(?P<series>[-\w ]+)/$', views.products, name='products'),
    url(r'^podguzniki/(?P<brand>[-\w ]+)/$', views.products, name='products'),


]