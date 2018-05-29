"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from polls.views import HomePageView, ImagePageView, CrearArchivoView, CrearArchivoCompletoView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('upload/', CrearArchivoCompletoView.as_view(), name='completoZip'),
    path('image/<token>', ImagePageView.as_view(), name='image'),
    path('upload/<token>', CrearArchivoView.as_view(), name='archivoZip')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
