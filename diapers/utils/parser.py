# coding=utf-8
import requests
import urllib2
from lxml import html, etree
from diapers.models import Brand, ProductPreview, Series, Seller, Stock, Product, Gender
from diapers.utils import common
import logging

import configparser

shop_xpath = configparser.ConfigParser()
shop_xpath.optionxform = str
shop_xpath.read('diapers/utils/shop_xpath.ini', encoding='utf-8')

shop_urls = configparser.ConfigParser()
shop_urls.optionxform = str
shop_urls.read('diapers/utils/shop_urls.ini', encoding='utf-8')


__author__ = 'anton.sorokoumov'

logger = logging.getLogger('compare')


def parse_catalog(seller, category_url, brand):
    # example_url = /catalog/pampers\

    next_url_xpath = shop_xpath[seller.name]['next_url_xpath']
    item_xpath = shop_xpath[seller.name]['item_xpath']
    item_title_xpath = shop_xpath[seller.name]['item_title_xpath']
    item_url_xpath = shop_xpath[seller.name]['item_url_xpath']
    next_url = [category_url]
    items_added = 0
    while next_url:
        next_url = next_url[0]
        next_url = seller.url + next_url
        page = requests.get(next_url)
        tree = html.fromstring(page.text)
        next_url = tree.xpath(next_url_xpath)
        items = tree.xpath(item_xpath)
        for item in items:
            item_title = item.xpath(item_title_xpath)
            item_url = item.xpath(item_url_xpath)
            if not Stock.objects.filter(url=item_url[0]):
                if seller.name == "Deti":
                    try:
                        description = item_title[0].decode('utf-8').encode('latin1')
                        ProductPreview(description=description, seller=seller, brand=brand,
                                       url=item_url[0],
                                       status="new").save()
                    except UnicodeEncodeError:
                        description = item_title[0]
                        ProductPreview(description=description, seller=seller, brand=brand,
                                       url=item_url[0],
                                       status="new").save()
                else:
                    description = u''.join(item_title)
                    ProductPreview(description=description, seller=seller, brand=brand, url=item_url[0],
                                   status="new").save()
                items_added += 1
    return items_added


def update_prices():
    # get prices from shops
    item_count = 0
    logger.debug('Updating prices...')
    stock_objects = Stock.objects.all()
    for stock_object in stock_objects:
        stock_object.is_visible = True
        logger.debug('Set visibility to true')

        product_url = stock_object.seller.url + stock_object.url
        price_xpath = shop_xpath[stock_object.seller.name]['price_xpath']
        # TODO            price_before_discount_xpath = ""
        try:
            page = requests.get(product_url)
            tree = html.fromstring(page.text)
            if not is_available(tree=tree, stock_object=stock_object):
                stock_object.is_visible = False
                stock_object.save()
                logger.debug('Stock object not available ' + str(stock_object.id) + ' ' + str(stock_object.url))
            price = tree.xpath(price_xpath)
            if stock_object.seller.name == "Ozon":
                price = price.replace(u'\xa0', '').encode('utf-8')
            else:
                price = price[0].replace(" ", "")
            try:
                stock_object.price_full = float(price)
                stock_object.price_unit = float(price) / stock_object.product.count
                stock_object.save()
            except ValueError:
                stock_object.is_visible = False
                stock_object.save()
                logger.debug('ValueError for stock_object ' + str(stock_object.id) + ' ' + str(stock_object.url))
        except (requests.exceptions.ReadTimeout, IndexError):
            stock_object.is_visible = False
            stock_object.save()
            logger.debug('ReadTimeout for stock_object ' + str(stock_object.id) + ' ' + str(stock_object.url))
        item_count += 1
    # TODO Price before discount
    return item_count


def is_available(tree, stock_object):
    unavailability_xpath = shop_xpath[stock_object.seller.name]['unavailability_xpath']
    if not tree.xpath(unavailability_xpath):
        return True
    else:
        return False


def parse_shop_catalog(seller_name):
    items_added = 0
    for brand in shop_urls[seller_name]:
        category_urls = [e.strip() for e in shop_urls[seller_name][brand].split(',')]
        for category_url in category_urls:
            items_added += parse_catalog(seller=Seller.objects.get(name=seller_name),
                                         brand=Brand.objects.get(name=brand),
                                         category_url=category_url)
    return items_added


def parse_shops_catalogs():
    items_added = 0
    for seller in shop_urls:
        items_added += parse_shop_catalog(seller)
    return items_added


def parse_ozon_catalog():
    catalog_url = shop_xpath['Ozon']['catalog_url']
    item_xpath = shop_xpath['Ozon']['item_xpath']
    url_xpath = shop_xpath['Ozon']['url_xpath']
    brand_xpath = shop_xpath['Ozon']['brand_xpath']
    description_xpath = shop_xpath['Ozon']['description_xpath']
    type_xpath = shop_xpath['Ozon']['type_xpath']
    items_added = 0
    seller = Seller.objects.get(name="Ozon")

    xml = urllib2.urlopen(catalog_url)
    tree = etree.parse(xml)
    offers = tree.xpath(item_xpath)
    for offer in offers:
        full_url = offer.xpath(url_xpath)
        url = full_url[0].replace(seller.url, "")
        brand = offer.xpath(brand_xpath)
        description = offer.xpath(description_xpath)
        item_type = offer.xpath(type_xpath)
        if item_type[0] in ["Многоразовый подгузник", "Подгузники", "Подгузники-трусики"]:
            if not Stock.objects.filter(url=url):
                try:
                    ProductPreview(description=description[0], seller=seller, brand=Brand.objects.get(name=brand[0]),
                                   series=Series.objects.get(name="!Unknown_Unknown_brand_Series"), url=url,
                                   status="new").save()
                    items_added += 1
                except (Brand.DoesNotExist, IndexError):
                    ProductPreview(description=description[0], seller=seller,
                                   brand=Brand.objects.get(name="Unknown_brand"),
                                   series=Series.objects.get(name="!Unknown_Unknown_brand_Series"), url=url,
                                   status="new").save()
                    items_added += 1
    return items_added


# TODO move all suggestions to the separate file
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
        description = product.description.split(" (")
        description = description[0].split(product.brand.name + " ")
        description = description[1].replace("Baby-Dry", "Baby")
        description = description.replace("Sleep&Play", "Sleep & Play")
        series = description.rsplit(' ', 1)[0]
        series = Series.objects.filter(name=series).first()
        try:
            return series.id
        except AttributeError:
            return "-1"
    elif product.seller == Seller.objects.get(name="Deti"):
        description = product.description.split(" кг")
        description = description[0].split(product.brand.name + " ")
        try:
            description = description[1].replace("Baby-Dry", "Baby")
        except IndexError:
            return "-1"
        description = description.replace("Sleep&Play", "Sleep & Play")
        series = description.rsplit(' ', 1)[0]
        series = Series.objects.filter(name=series).first()
        try:
            return series.id
        except AttributeError:
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
