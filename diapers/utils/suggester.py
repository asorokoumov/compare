# coding=utf-8
from diapers.utils import common
from diapers.models import Series, Seller, Gender, Type, Brand
from configobj import ConfigObj
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))

brand_list = ConfigObj(os.path.join(BASE, 'data_config/brands.ini'), encoding="UTF8")


def suggest_brand(product):
    brand = -1
    for brand in brand_list:
        if brand.strip().lower() in product.description.strip().lower():
            return Brand.objects.get(name=brand).id
    return brand


def suggest_series(product):
    all_series = []
    for brand in brand_list:
        for series in brand_list[brand]:
            all_series.append(series)
    for series in all_series:
        if series.strip().lower() in product.description.strip().lower():
            return Series.objects.get(name=series).id
    series = ''
    return series


def suggest_type(product):

    swim_words = [u'Плавания', u'плавания', 'Swim', 'swim']
    for word in swim_words:
        if product.description.find(word) != -1:
            result_type = Type.objects.filter(type='swim').first()
            return result_type.id
    pants_words = [u'Трусики', u'трусики', 'Pants', 'pants']
    for word in pants_words:
        if product.description.find(word) != -1:
            result_type = Type.objects.filter(type='pants').first()
            return result_type.id

    result_type = Type.objects.filter(type='diapers').first()
    return result_type.id


def suggest_gender(product):
    boys_words = [u'Мальчик', u'мальчик', 'Boy', 'boy']
    for word in boys_words:
        if product.description.find(word) != -1:
            result_gender = Gender.objects.filter(gender='male').first()
            return result_gender.id
    girls_words = [u'Девочек', u'девочек', 'Girl', 'girl', u'девочки']
    for word in girls_words:
        if product.description.find(word) != -1:
            result_gender = Gender.objects.filter(gender='female').first()
            return result_gender.id

    result_gender = Gender.objects.filter(gender='unisex').first()
    return result_gender.id


def suggest_size(product):
    if product.seller == Seller.objects.get(name="Korablik") or \
                    product.seller == Seller.objects.get(name="Akusherstvo"):
        size = product.description.split(" (")
        size = size[0].split(" ")
        return size[-1]
    elif product.seller == Seller.objects.get(name="Detmir"):
        return ""
    else:
        return ""


def suggest_min_weight(product):
    if product.seller == Seller.objects.get(name="Korablik") or \
                    product.seller == Seller.objects.get(name="Akusherstvo"):
        weight = common.find_between(product.description, "(", ")")
        weight = weight.replace(u'кг', "")
        weight = weight.replace(" ", "")
        weight = weight.split("-")
        weight = weight[0].replace("+", "")
        weight = weight.replace(",", ".")
        return weight
    elif product.seller == Seller.objects.get(name="Detmir"):
        if product.description.find('кг') != -1:
            split_by_weight = product.description.split(u'кг')
            split_by_space = (split_by_weight[0]).strip().split()
            split_by_space_last = split_by_space[-1:]
            split_by_space_last = split_by_space_last[0].replace("(", "")
            split_by_dash = split_by_space_last.split('-')
            if split_by_dash:
                return split_by_dash[-2:][0]
            else:
                return ''
    return ""


def suggest_max_weight(product):
    if product.seller == Seller.objects.get(name="Korablik") or \
                    product.seller == Seller.objects.get(name="Akusherstvo"):
        weight = common.find_between(product.description, "(", ")")
        weight = weight.replace(u'кг', "")
        weight = weight.replace(" ", "")
        weight = weight.split("-")
        try:
            weight = weight[1].replace(",", ".")
            return weight
        except IndexError:
            return "-1"
    elif product.seller == Seller.objects.get(name="Detmir"):
        if product.description.find('кг') != -1:
            split_by_weight = product.description.split(u'кг')
            split_by_space = (split_by_weight[0]).strip().split()
            split_by_space_last = split_by_space[-1:]
            split_by_space_last = split_by_space_last[0].replace("(", "")
            split_by_dash = split_by_space_last.split('-')
            if split_by_dash:
                return split_by_dash[-1:][0]
            else:
                return ''
    return ""


def suggest_count(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        count = common.find_between(product.description, ")", u'шт')
        count = count.replace(".", "")
        count = count.replace(" ", "")
        return count
    elif product.seller == Seller.objects.get(name="Detmir") or \
            product.seller == Seller.objects.get(name="Akusherstvo"):
        if product.description.find(u'шт') != -1:
            split_by_count = product.description.split(u'шт')
            split_by_space = split_by_count[0].split()
            result = split_by_space[-1:]
            if result:
                return result[0]
            else:
                return ''
    return ''
