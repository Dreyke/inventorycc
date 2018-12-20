from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from inventory.models import ProductInstance, Product, Flavor, Brand, Category
from django.views import generic
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .filters import ProductFilter, BrandFilter

@login_required
def index(request):
    """View function for home page of site"""

    # generate counts of some of the main objects
    num_products = connection.cursor()
    num_products.execute("SELECT count(*) FROM inventory_product")
    product_row = num_products.fetchone()

    # Available inventory
    num_instances_available = connection.cursor()
    num_instances_available.execute("SELECT count(*) FROM inventory_productinstance WHERE status = 'y'")
    instances_available_row = num_instances_available.fetchone()

    num_brands = connection.cursor()
    num_brands.execute("SELECT count(*) FROM inventory_brand")
    brand_row = num_brands.fetchone()

    low_inventory = connection.cursor()
    low_inventory.execute("SELECT count(*) FROM inventory_product WHERE inventory_amount < 30")
    low_inventory_dash = low_inventory.fetchone()


    context = {
        'num_products': product_row[0],
        'num_instances_available': instances_available_row[0],
        'num_brands': brand_row[0],
        'low_inventory': low_inventory_dash[0]
    }

    # render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class ProductListView(generic.ListView):
    template_name = 'product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 5

    # Function for the product list filter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        return context

    # Function for the product list pagination
    def get_queryset(self, *args, **kwargs):
        if self.kwargs:
            return Product.objects.filter(category=self.kwargs['category']).order_by('code')
        else:
            query = Product.objects.all().order_by('code')
            return query

class ProductDetailView(generic.DetailView):
    template_name = 'product_detail.html'
    model = Product
    context_object_name = 'product'

class BrandListView(generic.ListView):
    template_name = 'brand_list.html'
    model = Brand
    context_object_name = 'brands'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = BrandFilter(self.request.GET, queryset=self.get_queryset())
        return context

    # Function for the brand list pagination
    def get_queryset(self, *args, **kwargs):
        if self.kwargs:
            return Brand.objects.filter(category=self.kwargs['category']).order_by('brand_name')
        else:
            query = Brand.objects.all().order_by('brand_name')
            return query


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
    fields = '__all__'

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