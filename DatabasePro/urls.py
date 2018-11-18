"""DatabasePro URL Configuration

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
from django.conf.urls import url
from bookdeal import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.panel),
    url('front/', views.front),
    url('panel/', views.panel),
    url('market/', views.market),
    url('login/', views.login),
    url('info/', views.info),
    url('signup/', views.signup),
    url('signin/', views.login),
    url('addbook/', views.addbook),
    url('list_mysell', views.list_mysell)
    # url('deletebook/', views.delete_book),
    # url('index/', views.index),
    # url('newbook/', views.add_book),
# url('list_mysell', views.list_mysell),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
