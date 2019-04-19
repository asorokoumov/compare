# coding=utf-8

from diapers.models import Brand, Series, Product, Stock, Seller, Gender, Type, ProductPreview, PreviewParseHistory, Skip
from lxml import html
import requests
from configobj import ConfigObj
import re
import os.path
from django.http import HttpResponsePermanentRedirect
from diapers.utils import parser, suggester
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.db.models import Q


BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

shop_xpath = ConfigObj(os.path.join(BASE, 'utils/data_config/shop_xpath.ini'))
shop_urls = ConfigObj(os.path.join(BASE, 'utils/data_config/shop_urls.ini'))
brand_list = ConfigObj(os.path.join(BASE, 'utils/data_config/brands.ini'))


def admin(request):
    return render(request, 'diapers/admin.html')


#creates all brands from conf, if not existed
def update_brand_list(request):
    items_added = {}
    for brand in brand_list:
        items_added[brand] = Brand.objects.update_or_create(name=str(brand))
   # Series.set_default_data()
    return render(request, 'diapers/parse/update_brand_list.html', {'items_added': items_added})


# get all shops from db
# get all unparsed items from shops
def parse_shop_catalog(request):
    seller_name = request.GET.get('seller_name')
    items_added = {}
    if seller_name is None:
        sellers = Seller.objects.all()
        for seller in sellers:
            items_added[seller] = parser.parse_seller(seller)

    else:
        seller = Seller.objects.get(name=seller_name)
        items_added[seller] = parser.parse_seller(seller)
    return render(request, 'diapers/parse/parse_shop_catalog.html', {'items_added': items_added})


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
    if 'submit' in request.POST:
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
    elif 'skip' in request.POST:
        product_preview = ProductPreview.objects.filter(pk=request.POST['chosen_product_id']).first()
        product_preview.status = "skip"
        product_preview.save()
        skip = Skip(seller=product_preview.seller, url=product_preview.url)
        skip.save()

    return HttpResponsePermanentRedirect(reverse('diapers:manual'))


def manual_parse(request):
    prefiltered_products = ProductPreview.objects.filter(description__icontains='')

    chosen_products = prefiltered_products.filter(~Q(status='done'), ~Q(status='skip')).order_by('?')
   #chosen_products = ProductPreview.objects.filter(~Q(status='done'), ~Q(status='skip')).order_by('?')
    chosen_product = chosen_products.first()
    print '111-   ' + str(suggester.suggest_brand(chosen_product))
    print chosen_product.id
    return render(request, 'diapers/parse/manual_parse.html',
                  {'all_brands': Brand.objects.all(),
                   'all_series': Series.objects.filter(brand=suggester.suggest_brand(chosen_product)),
                   'all_types': Type.objects.all(),
                   'all_genders': Gender.objects.all(),
                   'suggest_brand': suggester.suggest_brand(chosen_product),
                   'suggest_series': suggester.suggest_series(chosen_product),
                   'suggest_size': suggester.suggest_size(chosen_product),
                   'suggest_type': suggester.suggest_type(chosen_product),
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


def recreate(request):
    # Delete products, previews and history from everywhere
   # PreviewParseHistory.objects.all().delete()
    ProductPreview.objects.all().delete()
    Product.objects.all().delete()
    # Seller recreate
    #  Seller.objects.all().delete()
    #  Seller.set_default_data()
    # Gender recreate
    Gender.objects.all().delete()
    Gender.set_default_data()
    # Brand recreate
    #  Brand.objects.all().delete()
    # Brand.set_default_data()
    # Series recreate
    Series.objects.all().delete()
    Series.set_default_data()
    # Type recreate
    Type.objects.all().delete()
    Type.set_default_data()
    # Series recreate
    #  items_added_korablik = parser.parse_shop_catalog('Korablik', False)
    #  items_added_detmir = parser.parse_shop_catalog('Detmir', False)

    return render(request, 'diapers/parse/recreate.html', {
        #      'items_added_korablik': items_added_korablik,
        #       'items_added_detmir': items_added_detmir,
        #      'items_added_ozon': items_added_ozon,
        #       'items_added': items_added_korablik + items_added_detmir  # + items_added_ozon
    })
