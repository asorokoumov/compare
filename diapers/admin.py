from django.contrib import admin

# Register your models here.
from .models import Series, Seller, Type, Gender, Product, Stock, Brand, ProductPreview
admin.site.register(Series)
admin.site.register(Seller)
admin.site.register(Type)
admin.site.register(Gender)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Brand)
admin.site.register(ProductPreview)

