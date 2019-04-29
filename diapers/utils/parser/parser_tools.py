# coding=utf-8

from selenium import webdriver
from configobj import ConfigObj
import os.path
import logging
import time
import requests
import crutch
from diapers.models import Brand, ProductPreview, Series, Seller, Stock, Skip
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


logger = logging.getLogger('compare')
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shop_xpath = ConfigObj(os.path.join(BASE, 'data_config/shop_xpath.ini'))
shop_urls = ConfigObj(os.path.join(BASE, 'data_config/shop_urls.ini'))
chrome_driver_path = os.path.join(BASE, 'chromedriver')
print chrome_driver_path


class CatalogParser:
    def __init__(self, headless, seller, is_next_url_full, scroll):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "none"

        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options,
                                       desired_capabilities=caps)
        self.driver.implicitly_wait(10) # seconds
        self.seller = seller
        self.scroll = scroll
        self.is_next_url_full = is_next_url_full
        self.items_checked = 0
        self.items_added = 0

        pass

    # parse category page on the seller's shop
    def parse_category(self, url):
        # example_url = /catalog/pampers\
        logger.debug('Parcing ' + self.seller.name + '. URL: ' + url)
        next_url = self.seller.url + url
        logger.debug(next_url)
        while next_url:
            try:
                next_url = self.parse_page(url=next_url)
                if not self.is_next_url_full:
                    next_url = self.seller.url + next_url
            except NoSuchElementException:
                logger.debug('ConnectionError ' + next_url)
                next_url = []
        logger.debug('Parsed: ' + str(self.items_checked))
        logger.debug('Added: ' + str(self.items_added))
        return self.items_checked, self.items_added

    def parse_page(self, url):
        self.driver.get(url)
        time.sleep(3)
        next_url = self.get_next_url()
        self.get_items()
        print ('checked ' + str(self.items_checked))
        print ('added ' + str(self.items_added))

        return next_url

    def get_next_url(self):
        if self.scroll:
            self.scroll_page()
        try:
            next_url = self.driver.find_element_by_xpath(shop_xpath[self.seller.name]['next_url_xpath']).get_attribute("href")
            logger.debug('next_url: ' + str(next_url))
        except NoSuchElementException, e:
            logger.debug("Couldn't find element during parsing items :" + str(e))
            next_url = []
        return next_url

    def get_items(self):
        logger.debug('getting items on page')
        try:
            items = self.driver.find_elements_by_xpath(shop_xpath[self.seller.name]['item_xpath'])
            for item in items:
                self.items_checked += 1
                item_title = item.find_element_by_xpath(shop_xpath[self.seller.name]['item_title_xpath']).text
                item_url = item.find_element_by_xpath(shop_xpath[self.seller.name]['item_url_xpath']).get_attribute("href")
                if not ProductPreview.objects.filter(url=item_url) and not Stock.objects.filter(
                        url=item_url) and not Skip.objects.filter(url=item_url):
                    description = u''.join(item_title)
                    ProductPreview(description=description, seller=self.seller, url=item_url,
                                   status="new").save()
                    self.items_added += 1
                else:
                    if Skip.objects.filter(url=item_url):
                        logger.debug('Skip has that url: ' + str(item_url))
                    elif Stock.objects.filter(url=item_url):
                        logger.debug('Stock has that url: ' + str(item_url))
                    elif ProductPreview.objects.filter(url=item_url):
                        logger.debug('ProductPreview has that url: ' + str(item_url))
                        self.items_checked += 1

        except NoSuchElementException, e:
            logger.debug("Couldn't find element during parsing items :" + str(e))

    def scroll_page(self):
        for x in range(3):
            self.driver.execute_script('window.scrollTo({top: document.body.scrollHeight, behavior: "smooth" });')
            time.sleep(1)

#        while True:
#            logger.debug('Scrolling')
#            items = self.driver.find_elements_by_xpath(shop_xpath[self.seller.name]['item_xpath'])
#
#            self.driver.execute_script('window.scrollTo({top: document.body.scrollHeight, behavior: "smooth" });')
#            time.sleep(1)
#            items_after_scroll = self.driver.find_elements_by_xpath(shop_xpath[self.seller.name]['item_xpath'])
#            if len(items) == len(items_after_scroll):
#                break


class ItemPageParser:

    def __init__(self, headless):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        options.add_argument('window-size=1200x600')
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
        self.driver.implicitly_wait(10)

        self.items_checked = 0
        pass


    def get_price(self, stock_object):
        try:
            self.driver.get(stock_object.url)
            price = self.driver.find_element_by_xpath(shop_xpath[stock_object.seller.name]['price_xpath']).text
            price = price.replace(" ", "")
            price = price.replace("&nbsp", "")
            price = price.replace(u"₽", "")
            logger.debug(price)

            # TODO add checking price before discount
            stock_object.price_full = float(price)
            stock_object.price_unit = float(price) / stock_object.product.count
            stock_object.is_visible = True
        except Exception as e:
            stock_object.is_visible = False
            logger.debug('ValueError during prices update for stock_object ' + str(stock_object.id) + ' '
                         + str(stock_object.url) + '  ' + str(e))
        return 1

