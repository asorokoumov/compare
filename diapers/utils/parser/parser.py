# coding=utf-8
import urllib2
from lxml import etree, html
from diapers.models import Brand, ProductPreview, Series, Seller, Stock
from parser_tools import *



BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

shop_xpath = ConfigObj(os.path.join(BASE, 'data_config/shop_xpath.ini'))
shop_urls = ConfigObj(os.path.join(BASE, 'data_config/shop_urls.ini'))

# chromedriver = ConfigObj(os.path.join(BASE, 'chromedriver'))


__author__ = 'anton.sorokoumov'

logger = logging.getLogger('compare')


def parse_seller(seller):
    if seller.name == 'Korablik':
        parser = CatalogParser(seller=seller, headless=False, is_next_url_full=True, scroll=False)
    elif seller.name == 'Ozon':
        parser = CatalogParser(seller=seller, headless=False, is_next_url_full=True, scroll=True)
    elif seller.name == 'Akusherstvo':
        parser = CatalogParser(seller=seller, headless=True, is_next_url_full=True, scroll=False)
    else:
        # Detmir
        parser = CatalogParser(seller=seller, headless=False, is_next_url_full=True, scroll=True)

    category_urls = shop_urls[seller.name]
    if type(category_urls) is str:
        category_urls = {category_urls}
    for category_url in category_urls:
        parser.parse_category(url=category_url)
    return parser.items_added



def get_prices_and_availability():

    # get prices from shops for stock
    item_count = 0
    logger.debug('Updating prices...')
    stock_objects = Stock.objects.all()
    parser = ItemPageParser(headless=True)
    for stock_object in stock_objects:
        logger.debug('Getting prices for ' + str(stock_object.id) + ' ' + str(stock_object.url))
        try:
            parser.get_price(stock_object=stock_object)

           # page = requests.get(stock_object.url)
           # tree = html.fromstring(page.text)
            # TODO add checking availability
#            stock_object.in_stock = is_in_stock(tree=tree, stock_object=stock_object)
           # get_item_prices(tree=tree, stock_object=stock_object)
        except (requests.exceptions.ReadTimeout, IndexError, requests.exceptions.ConnectionError) as e:
            logger.debug('Error during prices update for stock_object ' + str(stock_object.id) + ' '
                         + str(stock_object.url)+ '  ' + str(e))
            stock_object.is_visible = False

        stock_object.save()
        item_count += 1
    # TODO Price before discount
    return item_count


def get_item_prices(tree, stock_object):
    price = tree.xpath(shop_xpath[stock_object.seller.name]['price_xpath'])
    logger.debug(price[0])
    price = price[0].replace(" ", "")
    try:
        # TODO add checking price before discount
        stock_object.price_full = float(price)
        stock_object.price_unit = float(price) / stock_object.product.count
        stock_object.is_visible = True
    except ValueError as e:
        stock_object.is_visible = False
        logger.debug('ValueError during prices update for stock_object ' + str(stock_object.id) + ' '
                     + str(stock_object.url) + '  ' + str(e))


def is_in_stock(tree, stock_object):
    # TODO check it.
    unavailability_xpath = shop_xpath[stock_object.seller.name]['unavailability_xpath']
    if not tree.xpath(unavailability_xpath):
        return True
    else:
        logger.debug('Object is not in seller\'s stock ' + str(stock_object.id) + ' ' + str(stock_object.url))
        return False



def parse_shops_catalogs(check_stock=True):
    items_added = 0
    for seller in shop_urls:
        items_added += parse_seller(seller, check_stock=check_stock)
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


