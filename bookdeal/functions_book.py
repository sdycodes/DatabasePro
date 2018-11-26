from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *


def addbook(request):
    if request.method == 'GET':
        balance, saleSum = getBalance(request)
        return render(request, 'panel/addbook.html', {'balance': balance, 'saleSum': saleSum})
    if request.method == 'POST':
        book_name = request.POST.get('name')
        info = request.POST.get('info')
        price = float(request.POST.get('price'))
        cover = request.FILES.get('cover')
        balance, saleSum = getBalance(request)
        if book_name == "" or len(info) < 10 or price > 10000 or price < 0:
            return render(request, 'panel/index.html', {'TYPE':"Failure", 'msg':"Way too expensive and too little info given!", "username": request.user.username, 'balance': balance, 'saleSum': saleSum})
        if cover is None or cover.name.split('.')[1].lower() not in ['jpeg', 'jpg', 'png'] or cover.size > 10000000:
            return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "illegal cover", "username":request.user.username, 'balance': balance, 'saleSum': saleSum})
        Book.objects.create(name=book_name, info=info, price=price, cover=cover, owner=request.user)
        return render(request, 'panel/index.html', {'TYPE': "Success", 'msg': 'Successfully Add Book ' + book_name + '!', "username":request.user.username, 'balance': balance, 'saleSum': saleSum})


def getBalance(request):
    name = request.user.username
    orders = Order.objects.filter(buyer=name)
    try:
        useroutlet = Normal.objects.get(username=name)
    except Normal.DoesNotExist:
        try:
            useroutlet = Retailer.objects.get(username=name)
        except Retailer.DoesNotExist:
            return 0, 0
    sale_books = Book.objects.filter(owner=useroutlet)
    sales = Order.objects.filter(book_id__in=sale_books)
    balance = 0
    for sale in sales:
        if sale.isFinish:
            balance += sale.book_id.price
    return balance, len(sales)


def list_mysell(request):
    if request.method == 'GET':
        balance, saleSum = getBalance(request)
        book_id = request.GET.get('del')
        if book_id is not None:
            tar = Book.objects.filter(id=book_id, owner=request.user).order_by('id')
            if tar:
                book = tar[0]
                book.isDelete = True
                book.save()
                books = Book.objects.filter(owner=request.user, isDelete=False).order_by('id')
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'books': books,
                                                                  'TYPE': "Success",
                                                                  'msg': "delete successfully", 'balance': balance, 'saleSum': saleSum})
            books = Book.objects.filter(owner=request.user, isDelete=False).order_by('id')
            if books:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'TYPE': "Failure",
                                                                  'msg': "Error Occurred!", 'books': books, 'balance': balance, 'saleSum': saleSum})
            else:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'TYPE': "Warning",
                                                                  'msg': "You do not sell any single book!", 'balance': balance, 'saleSum': saleSum})
        else:
            books = Book.objects.filter(owner=request.user, isDelete=False).order_by('id')
            if books:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'books': books, 'balance': balance, 'saleSum': saleSum})
            else:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'TYPE': "Warning",
                                                                  'msg': "You do not sell any single book!", 'balance': balance, 'saleSum': saleSum})


def delete_book(request):
    if request.method == 'GET':
        return render(request, 'test/deletebook.html')
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        tar = Book.objects.filter(name=book_name, owner=request.user)
        if tar:
            book = tar[0]
            book.isDelete = True
            book.save()
            return render(request, 'test/result.html', {'func': 'delete_book', 'res': book.name})
        return render(request, 'test/result.html', {'func': 'delete_book', 'res': 'fail!'})
