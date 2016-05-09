# coding=utf-8
import requests
import urllib2
from lxml import html, etree
from diapers.models import Brand, ProductPreview, Series, Seller, Stock, Product, Gender
from diapers.utils import common
import logging

import configparser

shop_config = configparser.ConfigParser()
shop_config.read('diapers/utils/shop_config.ini', encoding='utf-8')


__author__ = 'anton.sorokoumov'

logger = logging.getLogger('compare')


def parse_catalog(seller, category_url, brand, series):
    # example_url = /catalog/pampers\

    next_url_xpath = shop_config[seller.name]['next_url_xpath']
    item_xpath = shop_config[seller.name]['item_xpath']
    item_title_xpath = shop_config[seller.name]['item_title_xpath']
    item_url_xpath = shop_config[seller.name]['item_url_xpath']
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
                        ProductPreview(description=description, seller=seller, brand=brand, series=series,
                                       url=item_url[0],
                                       status="new").save()
                    except UnicodeEncodeError:
                        description = item_title[0]
                        ProductPreview(description=description, seller=seller, brand=brand, series=series,
                                       url=item_url[0],
                                       status="new").save()
                else:
                    description = u''.join(item_title)
                    ProductPreview(description=description, seller=seller, brand=brand, series=series, url=item_url[0],
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
        price_xpath = shop_config[stock_object.seller.name]['price_xpath']
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
    unavailability_xpath = shop_config[stock_object.seller.name]['unavailability_xpath']

    if not tree.xpath(unavailability_xpath):
        return True
    else:
        return False



def parse_deti():
    # ## Deti
    # TODO move category urls to separate settings file
    # Pampers
    items_added = parse_catalog(seller=Seller.objects.get(name="Deti"),
                                brand=Brand.objects.get(name="Pampers"),
                                category_url="/catalog/gigiena/podguznikitrusiki/procter_end_gamble",
                                series=Series.objects.get(name="!Unknown_Pampers_Series"))
    # Huggies
    items_added += parse_catalog(seller=Seller.objects.get(name="Deti"),
                                 brand=Brand.objects.get(name="Huggies"),
                                 category_url="/catalog/gigiena/podguznikitrusiki/huggies",
                                 series=Series.objects.get(name="!Unknown_Huggies_Series"))
    # Libero
    items_added += parse_catalog(seller=Seller.objects.get(name="Deti"),
                                 brand=Brand.objects.get(name="Libero"),
                                 category_url="/catalog/gigiena/podguznikitrusiki/libero",
                                 series=Series.objects.get(name="!Unknown_Libero_Series"))
    # Goon
    items_added += parse_catalog(seller=Seller.objects.get(name="Deti"),
                                 brand=Brand.objects.get(name="Goon"),
                                 category_url="/catalog/gigiena/podguznikitrusiki/goon",
                                 series=Series.objects.get(name="!Unknown_Goon_Series"))
    # Helen Harper
    items_added += parse_catalog(seller=Seller.objects.get(name="Deti"),
                                 brand=Brand.objects.get(name="Helen Harper"),
                                 category_url="/catalog/gigiena/podguznikitrusiki/helen_harper",
                                 series=Series.objects.get(name="!Unknown_Pampers_Series"))
    # Baby care
    items_added += parse_catalog(seller=Seller.objects.get(name="Deti"),
                                 brand=Brand.objects.get(name="Baby care"),
                                 category_url="/catalog/gigiena/podguznikitrusiki/baby_care",
                                 series=Series.objects.get(name="!Unknown_Pampers_Series"))
    return items_added


def parse_korablik():
    # ## Korablik
    # TODO move category urls to separate settings file
    # TODO (check) Don't parse "Новинки" block
    # Pampers
    items_added = parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                brand=Brand.objects.get(name="Pampers"),
                                category_url="/catalog/pampers",
                                series=Series.objects.get(name="!Unknown_Pampers_Series"))
    # Huggies
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Huggies"),
                                 category_url="/catalog/huggies",
                                 series=Series.objects.get(name="!Unknown_Huggies_Series"))
    # Libero
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Libero"),
                                 category_url="/catalog/libero",
                                 series=Series.objects.get(name="!Unknown_Libero_Series"))
    # Maneki
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Huggies"),
                                 category_url="/catalog/maneki_maneki",
                                 series=Series.objects.get(name="!Unknown_Maneki_Series"))
    # Milly Tilly
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Milly Tilly"),
                                 category_url="/catalog/milly_tilly",
                                 series=Series.objects.get(name="!Unknown_Milly Tilly_Series"))
    # Goon
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Goon"),
                                 category_url="/catalog/goon",
                                 series=Series.objects.get(name="!Unknown_Goon_Series"))
    # Merries
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Merries"),
                                 category_url="/catalog/merries",
                                 series=Series.objects.get(name="!Unknown_Merries_Series"))
    # Moony
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Moony"),
                                 category_url="/catalog/moony",
                                 series=Series.objects.get(name="!Unknown_Moony_Series"))
    # Unknown - for swim
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Unknown_brand"),
                                 category_url="/catalog/podguzniki_dlya_plavaniya",
                                 series=Series.objects.get(name="!Unknown_Unknown_brand_Series"))
    # Unknown - gauze
    items_added += parse_catalog(seller=Seller.objects.get(name="Korablik"),
                                 brand=Brand.objects.get(name="Unknown_brand"),
                                 category_url="/catalog/marlevye_podguzniki",
                                 series=Series.objects.get(name="!Unknown_Unknown_brand_Series"))
    return items_added


def parse_detmir():
    # ## Detmir
    # TODO move category urls to separate settings file
    # Pampers
    items_added = parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                brand=Brand.objects.get(name="Pampers"),
                                category_url="/catalog/index/name/podguzniki/brand/2911/",
                                series=Series.objects.get(name="!Unknown_Pampers_Series"))
    # Goon
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name="Goon"),
                                 category_url="/catalog/index/name/podguzniki/brand/221/",
                                 series=Series.objects.get(name="!Unknown_Goon_Series"))
    # Huggies
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name="Huggies"),
                                 category_url="/catalog/index/name/podguzniki/brand/2921/",
                                 series=Series.objects.get(name="!Unknown_Huggies_Series"))
    # Libero
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name="Libero"),
                                 category_url="/catalog/index/name/podguzniki/brand/261/",
                                 series=Series.objects.get(name="!Unknown_Libero_Series"))
    # Mepsi
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name="Mepsi"),
                                 category_url="/catalog/index/name/podguzniki/brand/8151/",
                                 series=Series.objects.get(name="!Unknown_Mepsi_Series"))
    # Merries
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name="Merries"),
                                 category_url="/catalog/index/name/podguzniki/brand/821/",
                                 series=Series.objects.get(name="!Unknown_Merries_Series"))
    # Milly Tilly
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name="Milly Tilly"),
                                 category_url="/catalog/index/name/podguzniki/brand/7281/",
                                 series=Series.objects.get(name="!Unknown_Milly Tilly_Series"))
    # Пелигрин
    items_added += parse_catalog(seller=Seller.objects.get(name="Detmir"),
                                 brand=Brand.objects.get(name=u"Пелигрин"),
                                 category_url="/catalog/index/name/podguzniki/brand/4802/",
                                 series=Series.objects.get(name=u"!Unknown_Пелигрин_Series"))
    return items_added


def parse_ozon():
    # TODO move category urls to separate settings file

    catalog_url = "http://static.ozone.ru/multimedia/yml/facet/newborns_catalog/1175351.xml"
    item_xpath = "/yml_catalog/shop/offers/offer"
    url_xpath = "url/text()"
    brand_xpath = "vendor/text()"
    description_xpath = "name/text()"
    type_xpath = u"param[@name='Тип']/text()"
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
