__author__ = 'asorokoumov'
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<brand_id>[0-9]+)/$', views.brand, name='brand'),
    url(r'^(?P<brand_id>[0-9]+)/(?P<series_id>[0-9]+)/$', views.series, name='series'),

    url(r'^parse/korablik/$', views.parse_korablik, name='parse_korablik'),
]