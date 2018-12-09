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
from django.views import static
from django.conf import settings
from django.conf.urls import handler404, handler500

handler404 = views.page_not_found
handler500 = views.page_error


urlpatterns = [
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^cover/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),

    path('admin/', admin.site.urls),
    url(r'^$', views.login),
    url('panel', views.panel),
    url('detail', views.detail_report),
    url(r'^market/$', views.market),
    url('login', views.login),
    url('info', views.info),
    url('purchase', views.purchase),
    url('signup', views.signup),
    url('signin', views.login),
    url('manage', views.manage),
    url('settings', views.settings),
    url(r'^order/(.+)/(.+)/$', views.order),
    url(r'^report/(.+)/$', views.issue),
    url('report', views.list_myissue),
    url('addbook', views.addbook),
    url('addrlist', views.addrlist),
    url('list_mysell', views.list_mysell)
]
