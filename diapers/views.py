# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from lxml import html
import requests
import re
import logging

# Create your views here.
from diapers.models import Brand, Series, Product, Stock, Seller, Gender, Type, ProductPreview, PreviewParseHistory
from django.db.models import Q
from diapers.utils import parser, suggester
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import configparser


logger = logging.getLogger('compare')

shop_xpath = configparser.ConfigParser()
shop_xpath.optionxform = str
shop_xpath.read('diapers/utils/shop_xpath.ini', encoding='utf-8')

shop_urls = configparser.ConfigParser()
shop_urls.optionxform = str
shop_urls.read('diapers/utils/shop_urls.ini', encoding='utf-8')


def index(request):
    brands = Brand.objects.filter()

    return render(request, 'diapers/index.html', {'brands': brands})


def get_brand(request, brand_id):
    try:
        brand = Brand.objects.get(pk=brand_id)
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    return render(request, 'diapers/brand.html', {'brand': brand})


def get_series(request, brand_id, series_id):

    try:
        brand = Brand.objects.get(pk=brand_id)
        try:
            series = Series.objects.get(pk=series_id, brand=brand_id)
            products = Product.objects.filter(brand=brand_id, series=series_id).order_by('size', 'count')
        except Series.DoesNotExist:
            raise Http404("Series does not exist")
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    return render(request, 'diapers/series.html', {'brand': brand,
                                                   'series': series,
                                                   'products': products})


def parse_items(seller):
    seller_url = seller.url
    stock_items = Stock.objects.filter(seller=seller)

    for stock_item in stock_items:
        product_url = stock_item.url
        page = requests.get(seller_url + product_url)
        tree = html.fromstring(page.text)
        price_after_discount_xpath = shop_xpath[seller.name]['price_after_discount']
        price_after_discount = tree.xpath(price_after_discount_xpath)
        # TODO add price_before_discount
        # price_before_discount = tree.xpath('//span[@class="item-price"]/text()')
        try:
            price_after_discount = re.sub('\s+', '', price_after_discount[0])
            stock_item.price_full = price_after_discount
            stock_item.price_unit = float(price_after_discount) / stock_item.product.count
        except IndexError:
            stock_item.price_full = -1
            stock_item.price_unit = -1
        stock_item.save()


def manual_parse_result(request):
    new_product, created = Product.objects.get_or_create(
        name="New product",
        description="New product description",
        size=request.POST['size'],
        min_weight=request.POST['min_weight'],
        max_weight=request.POST['max_weight'],
        count=request.POST['count'],
        gender_id=request.POST['gender'],
        brand_id=request.POST['brand'],
        series_id=request.POST['series'],
        type_id=request.POST['type'])
    new_product.save()
    # TODO recheck types in parsed products
    # TODO check if there are same products with different stocks from one seller
    product_preview = ProductPreview.objects.filter(pk=request.POST['chosen_product_id']).first()
    product_preview.status = "Done"
    product_preview.save()

    preview_parse_history = PreviewParseHistory(product=new_product, preview=product_preview)
    preview_parse_history.save()

    new_stock, created = Stock.objects.get_or_create(seller=product_preview.seller, product=new_product,
                                                     url=product_preview.url,
                                                     defaults={'price_unit': -1, 'price_full': -1, 'in_stock': True,
                                                               'is_visible': True})

    new_stock.save()
    return HttpResponseRedirect(reverse('diapers:manual'))


def manual_parse(request):
    # TODO make for all other brands
    chosen_product = ProductPreview.objects.filter(~Q(status='Done'), brand=Brand.objects.get(name="Pampers")) \
        .order_by('?').first()

    return render(request, 'diapers/parse/manual_parse.html',
                  {'all_brands': Brand.objects.all(),
                   'all_series': Series.objects.all(),
                   'all_types': Type.objects.all(),
                   'all_genders': Gender.objects.all(),
                   'suggest_brand': suggester.suggest_brand(chosen_product),
                   'suggest_series': suggester.suggest_series(chosen_product),
                   'suggest_size': suggester.suggest_size(chosen_product),
                   'suggest_gender': suggester.suggest_gender(chosen_product),
                   'suggest_min_weight': suggester.suggest_min_weight(chosen_product),
                   'suggest_max_weight': suggester.suggest_max_weight(chosen_product),
                   'suggest_count': suggester.suggest_count(chosen_product),
                   'chosen_product': chosen_product,
                   'progress_counter': ProductPreview.objects.filter(~Q(status='Done'),
                                                                     brand=Brand.objects.get(name="Pampers")).count()})


def parse_prices(request):
    # TODO add availability checking
    prices_parsed = parser.update_prices()
    return render(request, 'diapers/parse/prices.html', {'prices_parsed': prices_parsed})


def recreate(request):
    # Delete products, previews and history from everywhere
    PreviewParseHistory.objects.all().delete()
    ProductPreview.objects.all().delete()
    # Seller recreate
    Seller.set_default_data()
    # Gender recreate
    Gender.set_default_data()
    # Brand recreate
    Brand.set_default_data()
    # Series recreate
    Series.set_default_data()
    # Type recreate
    Type.set_default_data()
    # Series recreate
    # TODO make separates buttons for each shop
    items_added_korablik = parser.parse_shop_catalog('Korablik')
    items_added_detmir = parser.parse_shop_catalog('Detmir')
    # TODO Ozon BROKEN!
#    items_added_ozon = parser.parse_ozon_catalog()
    # items_added_ozon = 0
    # TODO Check products, that already have parsed (compare urls, for example)

    return render(request, 'diapers/parse/recreate.html', {
        'items_added_korablik': items_added_korablik,
        'items_added_detmir': items_added_detmir,
 #      'items_added_ozon': items_added_ozon,
        'items_added': items_added_korablik  + items_added_detmir #+ items_added_ozon
    })
