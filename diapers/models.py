from django.db import models


# Create your models here.


class Brand (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Series (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.ForeignKey(Brand)

    def __str__(self):
        return self.name


class Seller (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Type (models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type


class Gender (models.Model):
    gender = models.CharField(max_length=200)

    def __str__(self):
        return self.gender


class Product (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.ForeignKey(Brand)
    series = models.ForeignKey(Series)
    type = models.ForeignKey(Type)
    gender = models.ForeignKey(Gender)
    size = models.CharField(max_length=200)
    min_weight = models.DecimalField(max_digits=10, decimal_places=2)
    max_weight = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField()

    def __str__(self):
        return self.name


class Stock (models.Model):
    seller = models.ForeignKey(Seller)
    product = models.ForeignKey(Product)
    url = models.TextField()
    price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    price_full = models.DecimalField(max_digits=10, decimal_places=2)

