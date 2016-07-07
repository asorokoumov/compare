# coding=utf-8
from django.http import Http404
from django.shortcuts import render
from lxml import html
import requests
import re
import logging
from diapers.models import Brand, Series, Product, Stock, Seller, Gender, Type, ProductPreview, PreviewParseHistory
from django.db.models import Q
from diapers.utils import parser, suggester
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from configobj import ConfigObj


logger = logging.getLogger('compare')

shop_xpath = ConfigObj('compare/diapers/utils/data_config/shop_xpath.ini')
shop_urls = ConfigObj('compare/diapers/utils/data_config/shop_urls.ini')


def index(request):
    return render(request, 'diapers/index.html')


def status(request):
    return render(request, 'diapers/status.html')


def todo(request):
    return render(request, 'diapers/todo.html')


def admin(request):
    return render(request, 'diapers/admin.html')


def show_brands(request):
    brands = Brand.objects.filter(~Q(name='Unknown_brand'))
    brand_output = []
    for brand in brands:
        if brand.name != 'Unknown_brand':
            if len(Stock.objects.filter(product=Product.objects.filter(brand=brand))):
                brand_output_item = {'series_count': len(Series.objects.filter(brand=brand)),
                                     'stock_count': len(Stock.objects.filter(product=Product.objects.filter(brand=brand))),
                                     'brand_id': brand.id,
                                     'brand_name': brand.name,
                                     'brand_image': brand.image}
                brand_output.append(brand_output_item)
                # TODO add brand.image
    brand_output.sort(key=lambda x: x['stock_count'], reverse=True)

    return render(request, 'diapers/brands.html', {'brand_output': brand_output})

# TODO show brands with no series


def show_series(request, brand_id):
    try:
        brand = Brand.objects.get(pk=brand_id)
        series_all = Series.objects.filter(brand=brand)
        series_output = []
        for series in series_all:
            if len(Stock.objects.filter(product=Product.objects.filter(series=series))) > 0:
                products = Product.objects.filter(brand=brand, series=series)
                sizes = products.values('size').distinct().count
                series_output_item = {'sizes_count': sizes,
                                      'stock_count': len(Stock.objects.filter(
                                          product=Product.objects.filter(series=series, brand=brand))),
                                      'series_name': series.name,
                                      'series_id': series.id}
                series_output.append(series_output_item)
        series_output.sort(key=lambda x: x['stock_count'], reverse=True)
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    return render(request, 'diapers/series.html', {'brand': brand, 'series_output': series_output})


def show_sizes(request, brand_id, series_id):
    try:
        brand = Brand.objects.get(pk=brand_id)
        series = Series.objects.get(pk=series_id, brand=brand)
        try:
            products = Product.objects.filter(series=series, brand=brand)
            sizes_objects = products.values('size').distinct()
            sizes = []
            for size_object in sizes_objects:
                sizes.append(size_object['size'])
            sizes.sort()
            sizes_output = []
            for size in sizes:
                products = Product.objects.filter(brand=brand, series=series, size=size)
                product_min_weight = min(products, key=lambda x: x.min_weight)
                product_max_weight = min(products, key=lambda x: x.min_weight)
                sizes_output_item = {'size_number': size,
                                     'stock_count': len(Stock.objects.filter(product=products)),
                                     'min_weight': product_min_weight.min_weight,
                                     'max_weight': product_max_weight.max_weight}
                sizes_output.append(sizes_output_item)

        except Series.DoesNotExist:
            raise Http404("Series does not exist")
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    sizes_output.sort(key=lambda x: x['min_weight'])
    return render(request, 'diapers/sizes.html', {'brand': brand,
                                                  'series': series,
                                                  'sizes_output': sizes_output})


def show_products(request, brand_id, series_id, size):
    try:
        brand = Brand.objects.get(pk=brand_id)
        try:
            series = Series.objects.get(pk=series_id, brand=brand_id)
            products = Product.objects.filter(brand=brand_id, series=series_id, size=size)
            stock_list = []
            for product in products:
                stock_objects = Stock.objects.filter(product=product)
                for stock_object in stock_objects:
                    if stock_object.is_visible:
                        stock_list.append(stock_object)
            stock_list.sort(key=lambda x: x.price_unit)
        except Series.DoesNotExist:
            raise Http404("Series does not exist")
    except Brand.DoesNotExist:
        raise Http404("Brand does not exist")
    return render(request, 'diapers/products.html', {'brand': brand,
                                                     'series': series,
                                                     'stock_list': stock_list,
                                                     'current_size': size})


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
        size=request.POST['size'],
        min_weight=request.POST['min_weight'],
        max_weight=request.POST['max_weight'],
        count=request.POST['count'],
        gender_id=request.POST['gender'],
        brand_id=request.POST['brand'],
        series_id=request.POST.get('series', None),
        type_id=request.POST['type'])
    new_product.save()
    product_preview = ProductPreview.objects.filter(pk=request.POST['chosen_product_id']).first()
    product_preview.status = "done"
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
    chosen_products = ProductPreview.objects.filter(~Q(status='done'), ~Q(status='skip')).order_by('?')
    chosen_product = chosen_products.first()

    return render(request, 'diapers/parse/manual_parse.html',
                  {'all_brands': Brand.objects.all(),
                   'all_series': Series.objects.filter(brand=chosen_product.brand),
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
                   'progress_counter': chosen_products.count()})


def update_prices_and_availability(request):
    # TODO add availability checking
    prices_parsed = parser.get_prices_and_availability()
    return render(request, 'diapers/parse/prices.html', {'prices_parsed': prices_parsed})


def update_product_list(request):
    items_added = {}
    shops = Seller.objects.all()
    for shop in shops:
        items_added[shop] = parser.parse_shop_catalog(shop, True)
    return render(request, 'diapers/parse/update_product_list.html', {'items_added': items_added})


def update_brand_list(request):
    brands = ConfigObj('diapers/utils/data_config/brands.ini')
    items_added = {}
    for brand in brands:
        items_added[brand] = Brand.objects.update_or_create(name=str(brand))
    return render(request, 'diapers/parse/update_brand_list.html', {'items_added': items_added})


def recreate(request):
    # Delete products, previews and history from everywhere
    #  PreviewParseHistory.objects.all().delete()
    #  ProductPreview.objects.all().delete()
    #  Product.objects.all().delete()
    # Seller recreate
    #  Seller.objects.all().delete()
    #  Seller.set_default_data()
    # Gender recreate
    #  Gender.objects.all().delete()
    #  Gender.set_default_data()
    # Brand recreate
    #  Brand.objects.all().delete()
    #  Brand.set_default_data()
    # Series recreate
    #  Series.objects.all().delete()
    #  Series.set_default_data()
    # Type recreate
    #  Type.objects.all().delete()
    #  Type.set_default_data()
    # Series recreate
    #  items_added_korablik = parser.parse_shop_catalog('Korablik', False)
    #  items_added_detmir = parser.parse_shop_catalog('Detmir', False)

    return render(request, 'diapers/parse/recreate.html', {
        #      'items_added_korablik': items_added_korablik,
        #       'items_added_detmir': items_added_detmir,
        #      'items_added_ozon': items_added_ozon,
        #       'items_added': items_added_korablik + items_added_detmir  # + items_added_ozon
    })
