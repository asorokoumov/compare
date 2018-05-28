# coding=utf-8
from diapers.utils import common
from diapers.models import Series, Seller, Gender
from configobj import ConfigObj
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))

brand_list = ConfigObj(os.path.join(BASE, 'data_config/brands.ini'))


def suggest_brand(product):
    brand = product.brand.id
    return brand


def suggest_series(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        description = product.description.split(" (")
        description = description[0].replace("Sleep&Play", "Sleep & Play")
        series = common.find_between(description, product.brand.name, suggest_size(product))
        series = series.strip()

        series = Series.objects.filter(name=series).first()
        try:
            return series.id
        except AttributeError:
            return "-1"
    elif product.seller == Seller.objects.get(name="Detmir"):
        # получить список всех серий
        all_series = []
        for series in brand_list[product.brand.name]:
            all_series.append(series)
        # найти первое совпадение серии у этого бренда
        # иначе предложить первую попавшуюся серию этого бренда
        suggested_series = '-1'
        for series in all_series:
            result = product.description.find(str(series))
            if result != -1:
                suggested_series = series
                print suggested_series

        if suggested_series == '-1':
            series_out = Series.objects.filter(brand=product.brand).first()
            suggested_series = all_series[0]
            print all_series
        else:
            series_out = Series.objects.filter(brand=product.brand, name=suggested_series).first()
            
        try:
            return series_out.id
        except AttributeError:
            print 'AttributeError - ' + str(suggested_series)
            return "-1"
    return "-1"


def suggest_type(product):
    return "1"


def suggest_gender(product):
    return Gender.objects.get(gender='unisex').id


def suggest_size(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        size = product.description.split(" (")
        size = size[0].split(" ")
        return size[-1]
    else:
        return ""


def suggest_min_weight(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        weight = common.find_between(product.description, "(", ")")
        weight = weight.replace(u'кг', "")
        weight = weight.replace(" ", "")
        weight = weight.split("-")
        weight = weight[0].replace("+", "")
        weight = weight.replace(",", ".")
        return weight
    else:
        return ""


def suggest_max_weight(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        weight = common.find_between(product.description, "(", ")")
        weight = weight.replace(u'кг', "")
        weight = weight.replace(" ", "")
        weight = weight.split("-")
        try:
            weight = weight[1].replace(",", ".")
            return weight
        except IndexError:
            return "-1"
    else:
        return ""


def suggest_count(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        count = common.find_between(product.description, ")", u'шт')
        count = count.replace(".", "")
        count = count.replace(" ", "")
        return count
    else:
        return ""
