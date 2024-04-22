from django.contrib import admin
from .models import Product, Country, Brand


class ProductAdmin(admin.ModelAdmin):
    pass


class CountryAdmin(admin.ModelAdmin):
    pass


class BrandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Brand, BrandAdmin)