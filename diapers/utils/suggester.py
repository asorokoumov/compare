# coding=utf-8
from diapers.utils import common
from diapers.models import Series, Seller, Gender, Type
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
        # найти первое совпадение серии у этого бренда
        # иначе предложить первую попавшуюся серию этого бренда

        all_series = []
        for series in brand_list[product.brand.name]:
            all_series.append(series)
        suggested_series = '-1'
        for series in all_series:
            result = product.description.find(str(series))
            if result != -1:
                suggested_series = series

        if suggested_series == '-1':
            series_out = Series.objects.filter(brand=product.brand).first()
            suggested_series = all_series[0]
        else:
            series_out = Series.objects.filter(brand=product.brand, name=suggested_series).first()

        try:
            return series_out.id
        except AttributeError:
            print 'AttributeError - ' + str(suggested_series)
            return "-1"
    return "-1"


def suggest_type(product):
    pants_words = ['Трусики', 'трусики', 'Pants', 'pants']
    for word in pants_words:
        if product.description.find(word) != -1:
            result_type = Type.objects.filter(type='pants').first()
            return result_type.id
    swim_words = ['Плавания', 'плавания', 'Swim', 'swim']
    for word in swim_words:
        if product.description.find(word) != -1:
            result_type = Type.objects.filter(type='swim').first()
            return result_type.id

    result_type = Type.objects.filter(type='diapers').first()
    return result_type.id


def suggest_gender(product):
    boys_words = ['Мальчиков', 'мальчиков', 'Boy', 'boy']
    for word in boys_words:
        if product.description.find(word) != -1:
            result_gender = Gender.objects.filter(gender='male').first()
            return result_gender.id
    girls_words = ['Девочек', 'девочек', 'Girl', 'girl']
    for word in girls_words:
        if product.description.find(word) != -1:
            result_gender = Gender.objects.filter(gender='female').first()
            return result_gender.id

    result_gender = Gender.objects.filter(gender='unisex').first()
    return result_gender.id


def suggest_size(product):
    if product.seller == Seller.objects.get(name="Korablik"):
        size = product.description.split(" (")
        size = size[0].split(" ")
        return size[-1]
    elif product.seller == Seller.objects.get(name="Detmir"):
        return ""
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
    elif product.seller == Seller.objects.get(name="Detmir"):
        if product.description.find('шт') != -1:
            split_by_count = product.description.split(u'шт')
            split_by_space = split_by_count[0].split()
            result = split_by_space[-1:]
            if result:
                return result[0]
            else:
                return ''
    return ''
