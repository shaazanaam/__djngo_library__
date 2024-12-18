"""
URL configuration for locallibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

]

# Use include() to add paths from the catalog application


# the text below ensures that whenever the URL pattern /catalog/ is encountered,
# the URL pattern is passed on to the catalog application for further processing.
urlpatterns += [path('catalog/', include('catalog.urls'))] 
# This line includes the URLconf for the catalog application

# Add URL maps to redirect the root URL to our application



urlpatterns += [path("", RedirectView.as_view(url="catalog/", permanent=True))]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add Django-site authentication urls (for login, logout, password management)
urlpatterns +=[path('accounts/', include('django.contrib.auth.urls')),]
 