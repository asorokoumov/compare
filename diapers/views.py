# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from lxml import html
import requests
import re

# Create your views here.
from diapers.models import Brand, Series, Product, Stock, Seller, Gender, Type, ProductPreview, PreviewParseHistory
from django.db.models import Q
from diapers.utils import parser
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


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
        page = requests.get(seller_url + product_url)
        tree = html.fromstring(page.text)

        price_after_discount = tree.xpath('//div[@class="goods-button-item_price"]/span[@class="num"]/text()')
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
                   'suggest_brand': parser.suggest_brand(chosen_product),
                   'suggest_series': parser.suggest_series(chosen_product),
                   'suggest_size': parser.suggest_size(chosen_product),
                   'suggest_gender': parser.suggest_gender(chosen_product),
                   'suggest_min_weight': parser.suggest_min_weight(chosen_product),
                   'suggest_max_weight': parser.suggest_max_weight(chosen_product),
                   'suggest_count': parser.suggest_count(chosen_product),
                   'chosen_product': chosen_product,
                   'progress_counter': ProductPreview.objects.filter(~Q(status='Done'),
                                                                     brand=Brand.objects.get(name="Pampers")).count()})


def parse_prices(request):
    # TODO BUG. Products disappear from the table on the web page
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
    items_added_korablik = parser.parse_korablik()
    # TODO Deti BROKEN!
    # items_added_deti = parser.parse_deti()
    items_added_deti = 0
    items_added_detmir = parser.parse_detmir()
    # TODO Ozon BROKEN!
    items_added_ozon = parser.parse_ozon()
    # items_added_ozon = 0
    # TODO Check products, that already have parsed (compare urls, for example)

    return render(request, 'diapers/parse/recreate.html', {
        'items_added_korablik': items_added_korablik,
        'items_added_deti': items_added_deti,
        'items_added_detmir': items_added_detmir,
        'items_added_ozon': items_added_ozon,
        'items_added': items_added_korablik + items_added_ozon + items_added_detmir + items_added_deti
    })
