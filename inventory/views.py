from django.shortcuts import render
from inventory.models import ProductInstance, Product, Flavor, Brand, Category
from django.views import generic
from django.db import connection, transaction
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
@login_required
def index(request):
    """View function for home page of site"""

    # generate counts of some of the main objects
    num_products = connection.cursor()
    num_products.execute("SELECT count(*) FROM inventory_product")
    product_row = num_products.fetchone()

    num_categories = connection.cursor()
    num_categories.execute("SELECT count(*) FROM inventory_category")
    category_row = num_categories.fetchone()

    # Available inventory
    num_instances_available = connection.cursor()
    num_instances_available.execute("SELECT count(*) FROM inventory_productinstance WHERE status = 'y'")
    instances_available_row = num_instances_available.fetchone()

    num_brands = connection.cursor()
    num_brands.execute("SELECT count(*) FROM inventory_brand")
    brand_row = num_brands.fetchone()


    context = {
        'num_products': product_row[0],
        'num_instances_available': instances_available_row[0],
        'num_brands': brand_row[0],
        'num_categories': category_row[0]
    }

    # render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class ProductListView(generic.ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 10

class ProductDetailView(generic.DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'

class BrandListView(generic.ListView):
    template_name = 'brand_list.html'
    model = Brand
    context_object_name = 'brands'
    paginate_by = 10


class BrandDetailView(generic.DetailView):
    template_name = 'brand_detail.html'
    model = Brand
    context_object_name = 'brand'

class BrandCreate(CreateView):
    template_name = 'brand_form.html'
    model = Brand
    fields = '__all__'

class BrandUpdate(UpdateView):
    template_name = 'brand_form.html'
    model = Brand
    fields = ['brand_name', 'website']

class BrandDelete(DeleteView):
    template_name = 'brand_confirm_delete.html'
    model = Brand
    success_url = reverse_lazy('brands')

class ProductCreate(CreateView):
    template_name = 'product_form.html'
    model = Product
    fields = '__all__'

class ProductUpdate(UpdateView):
    template_name = 'product_form.html'
    model = Product
    fields = '__all__'

class ProductDelete(DeleteView):
    template_name = 'product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('products')