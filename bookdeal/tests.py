from django.test import TestCase
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
# Create your tests here.


def index(request):
    return render(request, 'test/index.html')


def add_book(request):
    if request.method == 'GET':
        return render(request, 'test/addbook.html')
    if request.method == 'POST':
        book_name = request.POST.get('name')
        info = request.POST.get('info')
        price = float(request.POST.get('price'))
        cover = request.FILES.get('cover')
        if book_name == "" or len(info) < 10 or price > 10000 or price < 0:
            return render(request, 'test/result.html', {'func': 'add_book', 'res': 'illegal input !!'})
        if cover.name.split('.')[1].lower() not in ['jpeg', 'jpg', 'png'] or cover.size > 10000000:
            return render(request, 'test/result.html', {'func': 'add_book', 'res': 'illegal cover !!'})
        Book.objects.create(name=book_name, info=info, price=price, cover=cover, owner=request.user)
        return render(request, 'test/result.html', {'func': 'add_book', 'res': 'add success!'})


def search_book(request):
    tar = request.POST.get('name')
    res = Book.objects.filter(name__contains=tar)
    return render(request, 'test/list.html', {'func': 'search_book', 'res': res})


def signin(request):
    if request.method == 'GET':
        return render(request, 'test/signin.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        user = auth.authenticate(username=name, password=passwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            return render(request, 'test/result.html', {'func': 'signin', 'res': name})
        else:
            return render(request, 'test/result.html', {'func': 'signin', 'res': 'fail!'})


def my_car(request):
    user = request.user
    res = Car.objects.filter(owner=user)
    return render(request, 'test/list.html', {'func': 'my_car', 'res': res})


def add_car(request):
    user = request.user
    book_id = request.POST.get('id')
    check = Car.objects.filter(item=book_id, user=user)
    if check:
        return HttpResponse('already add')
    Car.objects.create(item=book_id, user=user)
    return HttpResponse('add successful')
