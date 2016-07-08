# coding=utf-8
import requests
import urllib2
from lxml import html, etree
from diapers.models import Brand, ProductPreview, Series, Seller, Stock
import logging
import crutch

from configobj import ConfigObj

shop_xpath = ConfigObj('compare/diapers/utils/data_config/shop_xpath.ini')
shop_urls = ConfigObj('compare/diapers/utils/data_config/shop_urls.ini')


__author__ = 'anton.sorokoumov'

logger = logging.getLogger('compare')


def parse_catalog(seller, category_url, brand, check_stock=True):
    # example_url = /catalog/pampers\
    logger.debug('Parcing ' + seller.name + '. Category: ' + category_url + '. Brand: ' + brand.name)
    next_url = [category_url]
    items_added = 0
    while next_url:
        next_url = next_url[0]
        next_url = seller.url + next_url
        try:
            page = requests.get(next_url)
            tree = html.fromstring(page.text)
            next_url = tree.xpath(shop_xpath[seller.name]['next_url_xpath'])
            next_url = crutch.next_url(next_url, seller)
            items = tree.xpath(shop_xpath[seller.name]['item_xpath'])
            for item in items:
                item_title = item.xpath(shop_xpath[seller.name]['item_title_xpath'])
                item_url = item.xpath(shop_xpath[seller.name]['item_url_xpath'])
                item_url[0] = crutch.item_url(item_url[0], seller)
                if not (any(ProductPreview.objects.filter(url=item_url[0])) & check_stock):
                    description = u''.join(item_title)
                    ProductPreview(description=description, seller=seller, brand=brand, url=item_url[0],
                                   status="new").save()
                    items_added += 1
        except ValueError:
            logger.debug('ConnectionError')
    logger.debug('Parced: ' + str(items_added))
    return items_added


def get_prices_and_availability():
    # get prices from shops for stock
    item_count = 0
    logger.debug('Updating prices...')
    stock_objects = Stock.objects.all()
    for stock_object in stock_objects:
        logger.debug('Getting prices for ' + str(stock_object.id) + ' ' + str(stock_object.url))
        try:
            page = requests.get(stock_object.seller.url + stock_object.url)
            tree = html.fromstring(page.text)
            # TODO add checking availability
#            stock_object.in_stock = is_in_stock(tree=tree, stock_object=stock_object)
            get_item_prices(tree=tree, stock_object=stock_object)
        except (requests.exceptions.ReadTimeout, IndexError):
            logger.debug('ReadTimeout during prices update for stock_object ' + str(stock_object.id) + ' '
                         + str(stock_object.url))
            stock_object.is_visible = False

        stock_object.save()
        item_count += 1
    # TODO Price before discount
    return item_count


def get_item_prices(tree, stock_object):
    price = tree.xpath(shop_xpath[stock_object.seller.name]['price_xpath'])
    price = price[0].replace(" ", "")
    try:
        # TODO add checking price before discount
        stock_object.price_full = float(price)
        stock_object.price_unit = float(price) / stock_object.product.count
        stock_object.is_visible = True
    except ValueError:
        stock_object.is_visible = False
        logger.debug('ValueError during prices update for stock_object ' + str(stock_object.id) + ' '
                     + str(stock_object.url))


def is_in_stock(tree, stock_object):
    # TODO check it.
    unavailability_xpath = shop_xpath[stock_object.seller.name]['unavailability_xpath']
    if not tree.xpath(unavailability_xpath):
        return True
    else:
        logger.debug('Object is not in seller\'s stock ' + str(stock_object.id) + ' ' + str(stock_object.url))
        return False


def parse_shop_catalog(seller, check_stock=True):
    items_added = 0
    for brand in shop_urls[seller.name]:
        category_urls = shop_urls[seller.name][brand]
        if type(category_urls) is str:
            category_urls = {category_urls}
        for category_url in category_urls:
            items_added += parse_catalog(seller=seller,
                                         brand=Brand.objects.get(name=brand),
                                         category_url=category_url, check_stock=check_stock)
    return items_added


def parse_shops_catalogs(check_stock=True):
    items_added = 0
    for seller in shop_urls:
        items_added += parse_shop_catalog(seller, check_stock=check_stock)
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


