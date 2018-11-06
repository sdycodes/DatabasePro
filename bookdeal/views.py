from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from bookdeal.models import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        # get the information
        name = request.POST.get('name')
        passwd1 = request.POST.get('password1')
        passwd2 = request.POST.get('password2')
        typ = request.POST.get('type')
        # check if they are legal
        if name == "" or passwd1 == "" or typ == "":
            return render(request, 'result.html', {'func': 'signup', 'res': 'cannot be null'})
        if passwd1 != passwd2:
            return render(request, 'result.html', {'func': 'signup', 'res': 'passwd not equal'})
        res = User.objects.filter(username=name)
        if res:
            return render(request, 'result.html', {'func': 'signup', 'res': 'name already exists!'})
        # sign up
        if typ == 'n':
            Normal.objects.create_user(username=name, password=passwd1)
        else:
            Retailer.objects.create_user(username=name, password=passwd1)
        return render(request, 'result.html', {'func': 'signup', 'res': 'success'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        user = auth.authenticate(username=name, password=passwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            return render(request, 'result.html', {'func': 'signin', 'res': name})
        else:
            return render(request, 'result.html', {'func': 'signin', 'res': 'fail!'})


def add_book(request):
    if request.method == 'GET':
        return render(request, 'addbook.html')
    if request.method == 'POST':
        book_name = request.POST.get('name')
        info = request.POST.get('info')
        price = float(request.POST.get('price'))
        cover = request.FILES.get('cover')
        if book_name == "" or len(info) < 10 or price > 10000 or price < 0:
            return render(request, 'result.html', {'func': 'add_book', 'res': 'illegal input !!'})
        if cover.name.split('.')[1].lower() not in ['jpeg', 'jpg', 'png'] or cover.size > 10000000:
            return render(request, 'result.html', {'func': 'add_book', 'res': 'illegal cover !!'})
        Book.objects.create(name=book_name, info=info, price=price, cover=cover, owner=request.user)
        return render(request, 'result.html', {'func': 'add_book', 'res': 'add success!'})


def list_mysell(request):
    books = Book.objects.filter(owner=request.user, isDelete=False)
    if books:
        return render(request, 'list.html', {'books': books})
    return render(request, 'result.html', {'func': 'list_mysell', 'res': 'None!'})


def delete_book(request):
    if request.method == 'GET':
        return render(request, 'deletebook.html')
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        tar = Book.objects.filter(name=book_name, owner=request.user)
        if tar:
            book = tar[0]
            book.isDelete = True
            book.save()
            return render(request, 'result.html', {'func': 'delete_book', 'res': book.name})
        return render(request, 'result.html', {'func': 'delete_book', 'res': 'fail!'})


def search_book(request):
    pass

