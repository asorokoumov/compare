# coding=utf-8
from django.db import models


# Create your models here.


class Brand (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

    @staticmethod
    def set_default_data():
        Brand.objects.update_or_create(name="Pampers", defaults={'description': "Pampers description"})
        Brand.objects.update_or_create(name="Huggies", defaults={'description': "Huggies description"})
        Brand.objects.update_or_create(name="Libero", defaults={'description': "Libero description"})
        Brand.objects.update_or_create(name="Maneki", defaults={'description': "Maneki description"})
        Brand.objects.update_or_create(name="Milly Tilly", defaults={'description': "Milly Tilly description"})
        Brand.objects.update_or_create(name="Goon", defaults={'description': "Goon description"})
        Brand.objects.update_or_create(name="Merries", defaults={'description': "Merries description"})
        Brand.objects.update_or_create(name="Moony", defaults={'description': "Moony description"})
        Brand.objects.update_or_create(name="Helen Harper", defaults={'description': "Helen Harper description"})
        Brand.objects.update_or_create(name="Baby care", defaults={'description': "Baby care description"})
        Brand.objects.update_or_create(name="Mepsi", defaults={'description': "Mepsi description"})
        Brand.objects.update_or_create(name=u"Пелигрин", defaults={'description': u"Пелигрин description"})
        Brand.objects.update_or_create(name="Unknown_brand", defaults={'description': "Unknown_brand description"})


class Series (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.ForeignKey(Brand)

    def __str__(self):
        return self.name

    @staticmethod
    def set_default_data():
        # Pampers Series
        Series.objects.update_or_create(name="Active Baby", brand=Brand.objects.get(name="Pampers"),
                                                       defaults={'description': "Active Baby description"})
        #TODO move description to defaults
        Series.objects.update_or_create(name="Active Boy", description="Active Boy description", brand=Brand.objects.get(name="Pampers"))
        Series.objects.update_or_create(name="Active girl", description="Active girl description", brand=Brand.objects.get(name="Pampers"))
        Series.objects.update_or_create(name="New Baby", description="New Baby description", brand=Brand.objects.get(name="Pampers"))
        Series.objects.update_or_create(name="Pants", description="Pants description", brand=Brand.objects.get(name="Pampers"))
        Series.objects.update_or_create(name="Premium Care", description="Premium Care description", brand=Brand.objects.get(name="Pampers"))
        Series.objects.update_or_create(name="Sleep & Play", description="Sleep & Play description", brand=Brand.objects.get(name="Pampers"))
        # Huggies Series
        Series.objects.update_or_create(name="Classic", description="Classic description", brand=Brand.objects.get(name="Huggies"))
        Series.objects.update_or_create(name="Elite Soft", description="Elite Soft description", brand=Brand.objects.get(name="Huggies"))
        Series.objects.update_or_create(name="Little Walkers", description="Little Walkers description",
               brand=Brand.objects.get(name="Huggies"))
        Series.objects.update_or_create(name="New Born", description="New Born description", brand=Brand.objects.get(name="Huggies"))
        Series.objects.update_or_create(name="Ultra Comfort", description="Ultra Comfort description",
               brand=Brand.objects.get(name="Huggies"))
        # Libero Series
        Series.objects.update_or_create(name="Comfort", description="Comfort description", brand=Brand.objects.get(name="Libero"))
        Series.objects.update_or_create(name="Dry Pants", description="Dry Pants description", brand=Brand.objects.get(name="Libero"))
        Series.objects.update_or_create(name="Every Day", description="Every Day description", brand=Brand.objects.get(name="Libero"))
        Series.objects.update_or_create(name="Newborn", description="Newborn description", brand=Brand.objects.get(name="Libero"))
        Series.objects.update_or_create(name="Up & Go", description="Up & Go description", brand=Brand.objects.get(name="Libero"))
        Series.objects.update_or_create(name="Swimpants", description="Swimpants description", brand=Brand.objects.get(name="Libero"))
        # Maneki Series
        Series.objects.update_or_create(name="Maneki no series", description="Maneki no series description",
               brand=Brand.objects.get(name="Maneki"))
        # Milly Tilly Series
        Series.objects.update_or_create(name="Milly Tilly no series", description="Milly Tilly no series description",
               brand=Brand.objects.get(name="Milly Tilly"))
        # Goon Series
        Series.objects.update_or_create(name="Goon no series", description="Goon no series description", brand=Brand.objects.get(name="Goon"))
        # Merries Series
        Series.objects.update_or_create(name="Merries no series", description="Merries no series description",
               brand=Brand.objects.get(name="Merries"))
        # Moony Series
        Series.objects.update_or_create(name="Moony no series", description="Moony no series description",
               brand=Brand.objects.get(name="Moony"))
        # Helen Harper
        Series.objects.update_or_create(name="Helen Harper no series", description="Helen Harper no series description",
               brand=Brand.objects.get(name="Helen Harper"))
        # Baby care
        Series.objects.update_or_create(name="Baby care no series", description="Baby care no series description",
               brand=Brand.objects.get(name="Baby care"))
        # Mepsi
        Series.objects.update_or_create(name="Mepsi no series", description="Mepsi no series description",
               brand=Brand.objects.get(name="Mepsi"))
        # Пелигрин
        Series.objects.update_or_create(name=u"Пелигрин no series", description=u"Пелигрин no series description",
               brand=Brand.objects.get(name=u"Пелигрин"))

        # Unknown
        Series.objects.update_or_create(name="!Unknown_Pampers_Series", description="Unknown_Pampers_Series",
               brand=Brand.objects.get(name="Pampers"))
        Series.objects.update_or_create(name="!Unknown_Huggies_Series", description="Unknown_Huggies_Series",
               brand=Brand.objects.get(name="Huggies"))
        Series.objects.update_or_create(name="!Unknown_Libero_Series", description="Unknown_Libero_Series",
               brand=Brand.objects.get(name="Libero"))
        Series.objects.update_or_create(name="!Unknown_Maneki_Series", description="Unknown_Maneki_Series",
               brand=Brand.objects.get(name="Maneki"))
        Series.objects.update_or_create(name="!Unknown_Milly Tilly_Series", description="Unknown_Milly Tilly_Series",
               brand=Brand.objects.get(name="Milly Tilly"))
        Series.objects.update_or_create(name="!Unknown_Goon_Series", description="Unknown_Goon_Series",
               brand=Brand.objects.get(name="Goon"))
        Series.objects.update_or_create(name="!Unknown_Merries_Series", description="Unknown_Merries_Series",
               brand=Brand.objects.get(name="Merries"))
        Series.objects.update_or_create(name="!Unknown_Moony_Series", description="Unknown_Moony_Series",
               brand=Brand.objects.get(name="Moony"))
        Series.objects.update_or_create(name="!Unknown_Baby care_Series", description="Unknown_Baby care_Series",
               brand=Brand.objects.get(name="Baby care"))
        Series.objects.update_or_create(name="!Unknown_Helen Harper_Series", description="Unknown_Helen Harper_Series",
               brand=Brand.objects.get(name="Helen Harper"))
        Series.objects.update_or_create(name="!Unknown_Mepsi_Series", description="Unknown_Mepsi_Series",
               brand=Brand.objects.get(name="Mepsi"))
        Series.objects.update_or_create(name=u"!Unknown_Пелигрин_Series", description=u"Unknown_Пелигрин_Series",
               brand=Brand.objects.get(name=u"Пелигрин"))
        Series.objects.update_or_create(name="!Unknown_Unknown_brand_Series", description="Unknown_Unknown_brand_Series",
               brand=Brand.objects.get(name="Unknown_brand"))


class Seller (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @staticmethod
    def set_default_data():
        #TODO move description and url to defaults
        Seller.objects.update_or_create(name="Korablik", description="Korablik description", url="http://korablik.ru")
        Seller.objects.update_or_create(name="Ozon", description="Ozon description", url="http://www.ozon.ru")
        Seller.objects.update_or_create(name="Deti", description="Deti description", url="http://online.detishop.ru")
        Seller.objects.update_or_create(name="Detmir", description="Detmir description", url="http://www.detmir.ru")


class Type (models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type

    @staticmethod
    def set_default_data():
        Type.objects.update_or_create(type="diapers")
        Type.objects.update_or_create(type="pants")
        Type.objects.update_or_create(type="swim")
        Type.objects.update_or_create(type="reusable")
        Type.objects.update_or_create(type="gauze")
        Type.objects.update_or_create(type="liners")


class Gender (models.Model):
    gender = models.CharField(max_length=200)

    def __str__(self):
        return self.gender

    @staticmethod
    def set_default_data():
        Gender.objects.update_or_create(gender="male")
        Gender.objects.update_or_create(gender="female")
        Gender.objects.update_or_create(gender="unisex")


class Product (models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    brand = models.ForeignKey(Brand)
    series = models.ForeignKey(Series)
    type = models.ForeignKey(Type)
    gender = models.ForeignKey(Gender)
    size = models.CharField(max_length=200)
    min_weight = models.FloatField()
    max_weight = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return self.name


class ProductPreview (models.Model):
    description = models.TextField()
    seller = models.ForeignKey(Seller)
    brand = models.ForeignKey(Brand)
    series = models.ForeignKey(Series)
    url = models.TextField()
    status = models.CharField(max_length=200)


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
    price_unit_is_min = models.BooleanField(default=False)
    in_stock = models.CharField(max_length=200)

