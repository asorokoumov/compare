# coding=utf-8
from django.db import models
from configobj import ConfigObj
import os.path

BASE = os.path.dirname(os.path.abspath(__file__))

basic = ConfigObj(os.path.join(BASE, 'utils/data_config/basic.ini'))
brands = ConfigObj(os.path.join(BASE, 'utils/data_config/brands.ini'))


class Brand (models.Model):
    name = models.CharField(max_length=200)
    url_name = models.CharField(max_length=200)
    description = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def set_default_data():
        for brand in brands:
            Brand.objects.update_or_create(name=str(brand))


class Series (models.Model):
    name = models.CharField(max_length=200)
    url_name = models.CharField(max_length=200)
    description = models.TextField(default=None, blank=True, null=True)
    brand = models.ForeignKey(Brand)

    def __str__(self):
        return "%s - %s" % (self.brand, self.name)

    @staticmethod
    def set_default_data():
        for brand in brands:
            for series in brands[brand]:
                Series.objects.update_or_create(name=series, brand=Brand.objects.get(name=str(brand)))


class Seller (models.Model):
    name = models.CharField(max_length=200)
    name_rus = models.CharField(max_length=200)
    description = models.TextField(default=None, blank=True, null=True)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @staticmethod
    def set_default_data():
        for base_gender in basic['Seller']:
            Seller.objects.update_or_create(gender=base_gender)


class Type (models.Model):
    type = models.CharField(max_length=200)
    type_rus = models.CharField(max_length=200)

    def __str__(self):
        return self.type

    @staticmethod
    def set_default_data():
        for base_type in basic['Type']:
            Type.objects.update_or_create(type=base_type)


class Gender (models.Model):
    gender = models.CharField(max_length=200)
    gender_rus = models.CharField(max_length=200)

    def __str__(self):
        return self.gender

    @staticmethod
    def set_default_data():
        for base_gender in basic['Gender']:
            Gender.objects.update_or_create(gender=base_gender)


class Product (models.Model):
    brand = models.ForeignKey(Brand)
    series = models.ForeignKey(Series, default=None)
    type = models.ForeignKey(Type)
    gender = models.ForeignKey(Gender)
    size = models.CharField(max_length=200)
    min_weight = models.FloatField()
    max_weight = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return "%s %s %s (%s - %s кг) %s шт" % \
               (self.brand, self.series, self.size, self.min_weight, self.max_weight, self.count)


class ProductPreview (models.Model):
    description = models.TextField()
    seller = models.ForeignKey(Seller)
    brand = models.ForeignKey(Brand)
    series = models.ForeignKey(Series, default=None, blank=True, null=True)
    url = models.TextField()
    status = models.CharField(max_length=200)

    def __str__(self):
        return "%s %s %s - %s " % \
               (self.seller, self.brand, self.series, self.status)


class PreviewParseHistory (models.Model):
    product = models.ForeignKey(Product)
    preview = models.ForeignKey(ProductPreview)


class Stock (models.Model):
    seller = models.ForeignKey(Seller)
    product = models.ForeignKey(Product)
    url = models.TextField()
    price_unit = models.FloatField()
    price_full = models.FloatField()
    price_unit_before_discount = models.FloatField(default=-1)
    price_full_before_discount = models.FloatField(default=-1)
    in_stock = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)  # = False if we have any errors during price parcing


class Skip (models.Model):
    seller = models.ForeignKey(Seller)
    url = models.TextField()


