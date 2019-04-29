# coding=utf-8
from django.http import Http404
from django.shortcuts import render

from diapers.models import Brand, Series, Product, Stock
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import simplejson
from diapers.utils.parser import crutch


def index(request):
#    brands = Brand.objects.filter(~Q(name='Unknown_brand')).order_by('name')
    brands = Brand.objects.filter(Q(name='Pampers'), Q(name='Huggies'),)
    for brand in brands:
        if not len(Stock.objects.filter(product=Product.objects.filter(brand=brand))):
            brands = brands.filter(~Q(pk=brand.id))
    brands = brands.order_by('name')
    sizes = []
    series = []
    return render(request, 'diapers/index.html', {'brands': brands, 'series': series, 'sizes': sizes})


def redirect_to_index(request):
    return HttpResponsePermanentRedirect(reverse('diapers:index'))


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



def get_series(request, brand_id):
    if brand_id != '-1':
        brand = Brand.objects.get(pk=brand_id)
        series = Series.objects.filter(~Q(name='No series'), ~Q(name='Без серии'), brand=brand)
    else:
        series = Series.objects.filter(~Q(name='Unknown_series'), ~Q(name='No series'), ~Q(name='Без серии')).order_by('name')
    series_dict = {}
    for series_item in series:
        series_dict[series_item.id] = series_item.name
    return HttpResponse(simplejson.dumps(series_dict), content_type="application/json")


def get_sizes(request, brand_id, series_id):
    if brand_id != '-1':
        brand = Brand.objects.get(pk=brand_id)
        if series_id != '-1':
            series = Series.objects.filter(brand=brand, id=series_id)
            sizes_products = Product.objects.values('size').filter(brand=brand, series=series).distinct().order_by('size')
        else:
            sizes_products = Product.objects.values('size').filter(brand=brand).distinct().order_by('size')
    else:
        if series_id != '-1':
            series = Series.objects.filter(id=series_id)
            sizes_products = Product.objects.values('size').filter(series=series).distinct().order_by('size')
        else:
            sizes_products = Product.objects.values('size').distinct().order_by('size')
    sizes = []
    for size in sizes_products:
        sizes.append(size['size'])
    sizes.sort()
    return HttpResponse(simplejson.dumps(sizes), content_type="application/json")


def get_brands(request, brand_id, series_id):
    brands_dict = {}
    if brand_id == '-1':
        for br in Brand.objects.all():
            series = Series.objects.filter(brand=br, id=series_id)
            if series:
                brands_dict[br.id] = br.name
    else:
        br = Brand.objects.get(pk=brand_id)
        brands_dict[br.id] = br.name
    return HttpResponse(simplejson.dumps(brands_dict), content_type="application/json")


def search(request):
    kwargs = {}
    try:
        brand_id = request.POST.get('brand', False)
        brand = Brand.objects.get(pk=brand_id)
        kwargs['brand'] = brand.url_name
    except Brand.DoesNotExist:
        kwargs['brand'] = 'NoBrand'

    try:
        series_id = request.POST.get('series', False)
        series = Series.objects.get(pk=series_id)
        kwargs['series'] = series.url_name
    except Series.DoesNotExist:
        kwargs['series'] = 'NoSeries'

    size = request.POST.get('size', '-1')
    if not size == '-1':
        kwargs['size'] = crutch.decode_url(size)

    return HttpResponsePermanentRedirect(reverse('diapers:products', kwargs=kwargs))


def products(request, brand='NoBrand', series='NoSeries', size='NoSize'):

    # header
    header = {}
    if not brand == 'NoBrand':
        header['brand'] = Brand.objects.get(url_name=brand)
    if not series == 'NoSeries':
        header['series'] = Series.objects.get(url_name=series)
    if not size == 'NoSize':
        header['size'] = crutch.encode_url(size)

    # search products
    product_list = Product.objects.all()
    if not brand == 'NoBrand':
        brand_id = Brand.objects.get(url_name=brand)
        product_list = product_list.filter(brand=brand_id)
    if not series == 'NoSeries':
        series_id = Series.objects.get(url_name=series)
        product_list = product_list.filter(series=series_id)
    if not size == 'NoSize':
        product_list = product_list.filter(size=crutch.encode_url(size))
    stock_list = []
    for product in product_list:
        stock_objects = Stock.objects.filter(product=product)
        for stock_object in stock_objects:
            if stock_object.is_visible:
                stock_list.append(stock_object)
    stock_list.sort(key=lambda x: x.price_unit)
    try:
        best = stock_list[0]
        profit_rub = stock_list[-1].price_unit - stock_list[0].price_unit
        profit_percent = 100 - stock_list[0].price_unit * 100 / stock_list[-1].price_unit
    except IndexError:
        best = []
        profit_rub = ''
        profit_percent = ''

    return render(request, 'diapers/products.html', {'header': header, 'stock_list': stock_list, 'best': best,
                                                     'profit_rub': profit_rub, 'profit_percent': profit_percent})