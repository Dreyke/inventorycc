from django.contrib import admin
from inventory.models import Category, Brand, Product, ProductInstance, Flavor

# Register your models here.
admin.site.register(Category)
# admin.site.register(Brand)
#admin.site.register(Product)
admin.site.register(ProductInstance)
admin.site.register(Flavor)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'website')

# register the admin class with the associated model
admin.site.register(Brand, BrandAdmin)

#register the admin classes for Product using decorator
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'brand', 'list_price', 'inventory_amount', 'date_added' )
