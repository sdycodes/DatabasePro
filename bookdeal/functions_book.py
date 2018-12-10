from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
from bookdeal.views import *
from bookdeal.functions_trans import *
from bookdeal.functions_car import *
from bookdeal.functions_user import *
from django.contrib.auth.decorators import login_required


# 最优 一次查表 计算总交易额
def getBalance():
    sales = len(Order.objects.all())
    balance = Order.objects.select_related('book_id').aggregate(Sum('book_id__price'))
    balance = balance['book_id__price__sum'] if balance['book_id__price__sum'] else 0
    return balance, sales


# 用户类型判断优化
@login_required
def market(request):
    tar = request.POST.get('name')
    q = request.GET.get('q')
    user = request.user
    balance, saleSum = getBalance()
    if tar is None and q is None:
        return render(request, 'panel/market.html', {'username': request.user.username, 'balance': balance, 'saleSum': saleSum})
    else:
        if q is None:
            q = tar
        books = Book.objects.filter(name__contains=q, isDelete=False).exclude(name__contains=q, isDelete=False, owner=user).order_by('id')
        paginator = Paginator(books, 2)  # Show 2 contacts per page

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            books = paginator.page(paginator.num_pages)
        add = request.GET.get('add')
        if add:
            if not user or user.first_name=='g':
                return render(request, 'panel/index.html',
                              {'username': request.user.username, 'TYPE': "Warning",
                               'msg': "Please Login As User First!"})
            elif user.first_name == 'a':
                return render(request, 'panel/index.html',
                              {'username': request.user.username, 'TYPE': "Failure",
                               'msg': "Retailers Not Authorized to Purchase!", 'balance': balance, 'saleSum': saleSum})

            useroutlet = user.normal
            check = Car.objects.filter(user=useroutlet, item=add)
            if check:
                return render(request, 'panel/market.html',
                              {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Failure",
                               'msg': "Add to Cart Failed, Book Exists!", 'balance': balance, 'saleSum': saleSum})

            Car.objects.create(item=add, user=useroutlet)
            return render(request, 'panel/market.html',
                          {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Success", 'msg': "Add to Cart Successfully!", 'balance': balance, 'saleSum': saleSum})
        if q is not None and books is None:
            return render(request, 'panel/market.html', {'username': request.user.username, 'books': books, 'query': q, 'balance': balance, 'saleSum': saleSum, 'TYPE': "Failure", 'msg': "Failed to find any related books!"})
        elif q is not None and books is not None:
            return render(request, 'panel/market.html',
                          {'username': request.user.username, 'books': books, 'query': q, 'balance': balance,
                           'saleSum': saleSum, 'TYPE': "Success", 'msg': "Browse books from recommended list!"})
        else:
            return render(request, 'panel/market.html',
                          {'username': request.user.username, 'books': books, 'query': q, 'balance': balance,
                           'saleSum': saleSum, 'TYPE': "Success", 'msg': "Welcome to the market!"})


# 最优
@login_required
def addbook(request):
    if request.method == 'GET':
        balance, saleSum = getBalance()
        return render(request, 'panel/addbook.html', {"username": request.user.username, 'balance': balance, 'saleSum': saleSum})
    if request.method == 'POST':
        user = request.user
        book_name = request.POST.get('name')
        info = request.POST.get('info')
        price = float(request.POST.get('price'))
        cover = request.FILES.get('cover')
        balance, saleSum = getBalance()
        names = ""
        if user.first_name == 'n' and user.normal.dept and user.normal.grade:
            rlist = Rlist.objects.filter(dept=user.normal.dept, grade=user.normal.grade)
            if rlist:
                names = rlist[0].names
        if book_name == "" or len(info) < 10 or price > 10000 or price < 0:
            return render(request, 'panel/index.html', {'names': names, 'TYPE':"Failure", 'msg':"Way too expensive or too little info given!", "username": request.user.username, 'balance': balance, 'saleSum': saleSum})
        if cover is None or cover.name.split('.')[-1].lower() not in ['jpeg', 'jpg', 'png'] or cover.size > 10000000:
            return render(request, 'panel/index.html', {'names': names, 'TYPE': "Warning", 'msg': "illegal cover", "username":request.user.username, 'balance': balance, 'saleSum': saleSum})
        Book.objects.create(name=book_name, info=info, price=price, cover=cover, owner=request.user)
        return render(request, 'panel/index.html', {'names': names, 'TYPE': "Success", 'msg': 'Successfully Add Book ' + book_name + '!', "username": request.user.username, 'balance': balance, 'saleSum': saleSum})


# 最优
@login_required
def list_mysell(request):
    if request.method == 'GET':
        balance, saleSum = getBalance()
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

