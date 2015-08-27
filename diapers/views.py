from django.views import generic
from django.http import Http404
from django.shortcuts import render
from lxml import html
import requests
import re

# Create your views here.
from diapers.models import Brand, Series, Product, Stock, Seller


def index(request):
    brands = Brand.objects.filter()

    return render(request, 'diapers/index.html', {'brands': brands})


def brand(request, brand_id):
    try:
        brand = Brand.objects.get(pk=brand_id)
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    return render(request, 'diapers/brand.html', {'brand': brand})


def series(request, brand_id, series_id):
    try:
        brand = Brand.objects.get(pk=brand_id)
        try:
            series = Series.objects.get(pk=series_id, brand=brand_id)
            products = Product.objects.filter(brand=brand_id, series=series_id)
        except Series.DoesNotExist:
            raise Http404("Series does not exist")
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    return render(request, 'diapers/series.html', {'brand': brand,
                                                   'series': series,
                                                   'products': products})


def parse_korablik(request):
    seller_id = 4
    parse(seller_id)
    prices = Stock.objects.filter(seller=seller_id)

    return render(request, 'diapers/parse/korablik.html', {'price_after_discount': prices})


def parse(seller_id):
    seller_url = Seller.objects.get(pk=seller_id).url
    stock_items = Stock.objects.filter(seller=seller_id)

    for stock_item in stock_items:
        product_url = stock_item.url
        page = requests.get(seller_url+product_url)
        tree = html.fromstring(page.text)

        price_after_discount = tree.xpath('//div[@class="goods-button-item_price"]/span[@class="num"]/text()')
        #TODO add price_before_discount
        #price_before_discount = tree.xpath('//span[@class="item-price"]/text()')
        try:
            price_after_discount = re.sub('\s+', '', price_after_discount[0])
            stock_item.price_full = price_after_discount
            stock_item.price_unit = float(price_after_discount)/stock_item.product.count
        except IndexError:
            stock_item.price_full = -1
            stock_item.price_unit = -1
        stock_item.save()

