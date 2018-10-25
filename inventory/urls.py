from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('brands/', views.BrandListView.as_view(), name='brands'),
    path('brand/<int:pk>', views.BrandDetailView.as_view(), name='brand-detail')
]

urlpatterns += [
    path('brand/create/', views.BrandCreate.as_view(), name='brand-create'),
    path('brand/<int:pk>/update/', views.BrandUpdate.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete/', views.BrandDelete.as_view(), name='brand-delete'),
]

urlpatterns += [
    path('product/create/', views.ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/update/', views.ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', views.ProductDelete.as_view(), name='product-delete'),
]