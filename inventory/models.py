from django.db import models
from django.urls import reverse
import uuid
from decimal import Decimal

# Create your models here.
class Category(models.Model):
    """Model representing the inventory category"""
    name = models.CharField(max_length=200, help_text='Enter the product category (e.g. Pre-Workout)')

    def __str__(self):
        """String for representing the Model object"""
        return self.name

class Flavor(models.Model):
    """Model representing available flavors"""
    flavor = models.CharField('Flavor', max_length=200, help_text="Enter available flavors")

    def __str__(self):
        """String for representing the Model object"""
        return self.flavor

class Product(models.Model):
    """Model representing different supplement inventory"""
    name = models.CharField(max_length=200)

    # foreign key used because each product can only have one brand, but brands can have multiple inventory
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, null=True)

    code = models.CharField('Product Code', max_length=10, help_text='Must be first 4 characters of the brand followed by yy-mm-dd')
    description = models.TextField(max_length=200, help_text="Enter a brief description of the product")
    list_price = models.DecimalField(max_digits=5, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=3, decimal_places=0)
    serving_size = models.IntegerField(help_text="Enter product serving size.")
    inventory_amount = models.IntegerField(help_text="Enter inventory amount for product.")
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True)
    product_image = models.ImageField(max_length=255, upload_to='product_images/%Y/%m/%d/', null=True, blank=True)

    # ManyToManyField used because categories and flavors can contain different inventory. Products can cover different categories.
    category = models.ManyToManyField(Category, help_text="Select a category for this product")
    flavors = models.ManyToManyField(Flavor, help_text="Select available flavors for this product")

    # field for user to enter custom data
    custom_field = models.CharField(max_length=100, null=True)
    def __str__(self):
        """String for representing Model object"""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this product"""
        return reverse('product-detail', args=[str(self.id)])

    @property
    def total_price(self):
        """Returns the final price calculated from list price and discount percent"""
        final_price = (self.list_price - (self.discount_percent / 100) * self.list_price)
        return round(final_price, 2)

class ProductInstance(models.Model):
    """Model representing a specific copy of a product"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this product.")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)


    stock = [
        ('y', 'In Stock'),
        ('n', 'Out of Stock'),
    ]

    status = models.CharField(
        max_length=1,
        choices=stock,
        blank=True,
        default='n',
        help_text="Product Availability",
    )

    class Meta:
        permissions = (("can_mark_stock", "Set product as in stock"),)

    def stock_status(self):
        if Product.inventory_amount < 1:
           self.status = 'y'
        else:
            self.status = 'n'
        return self.stock_status

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.id} ({self.product})'

class Brand(models.Model):

    """Model representing product brand"""
    brand_name = models.CharField(max_length=100)
    website = models.URLField(max_length=100)

    def get_absolute_url(self):
        """returns the url to access a brand instance"""
        return reverse('brand-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.brand_name}'