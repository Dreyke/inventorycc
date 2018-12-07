"""midtermproject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from inventory.forms import LoginForm
from django.contrib.auth import views as auth_views

# uses include() to add paths from the inventory app
# add url maps to redirect the base URL to app
# use static() to add url mapping to serve static files during development (only)
urlpatterns = [
    path('login/', auth_views.auth_login, {'authentication_form':LoginForm}),
    path('logout/', auth_views.auth_logout, name='logout'),
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('', RedirectView.as_view(url='/inventory/')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)