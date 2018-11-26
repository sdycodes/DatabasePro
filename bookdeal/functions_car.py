from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
from bookdeal.views import *


def addcar(request):
    user = request.user
    book_id = request.POST.get('id')
    check = Car.objects.filter(item=book_id, user=user)
    if check:
        return HttpResponse('Already Add This Book!')
    Car.objects.create(item=book_id, user=user)
    return HttpResponse('Add Successfully!')


def removecar(request):
    user = request.user
    book_id = request.POST.get('id')
    check = Car.objects.filter(item=book_id, user=user)
    if check:

        return HttpResponse('Add Successfully!')


def info(request):
    purchased = False
    if request.user.username and Admin.objects.filter(username=request.user.username):
        return manage(request)
    if request.method == 'POST':
        checks = request.POST.getlist('checkRow')
        if checks:
            buyer = request.user.username
            print(checks)
            for id in checks:
                book = Book.objects.filter(id=id, isDelete=False).order_by('id')
                if book:
                    book = book[0]
                book.isDelete = False
                book.save()
                Order.objects.create(buyer=buyer, book_id=book, isFinish=False)
                useroutlet = Normal.objects.get(username=buyer)
                Car.objects.get(item=id, user=useroutlet).delete()
                purchased = True

    name = request.user.username
    balance, saleSum = getBalance(request)
    orders = Order.objects.filter(buyer=name)
    try:
        useroutlet = Normal.objects.get(username=name)
    except Normal.DoesNotExist:
        try:
            useroutlet = Retailer.objects.get(username=name)
            sale_books = Book.objects.filter(owner=useroutlet)
            sales = Order.objects.filter(book_id__in=sale_books)
            return render(request, 'panel/info.html', {'username': request.user.username, 'retail': True, 'orders': orders, 'orderSum': len(orders), 'sales': sales, 'saleSum': saleSum, 'balance': balance})
        except Retailer.DoesNotExist:
            return render(request, 'panel/index.html',
                          {'username': request.user.username, 'TYPE': "Warning",
                           'msg': "Please Login First!"})
    sale_books = Book.objects.filter(owner=useroutlet)
    sales = Order.objects.filter(book_id__in=sale_books)
    ids = Car.objects.filter(user=useroutlet)
    idset = []
    for idi in ids:
        idset.append(idi.item)
    books = Book.objects.filter(id__in=idset, isDelete=False).order_by('id')
    paginator = Paginator(books, 3)  # Show 2 contacts per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)
    delete = request.GET.get('del')
    if delete:
        useroutlet = Normal.objects.get(username=name)
        check = Car.objects.filter(user=useroutlet, item=delete)
        if not check:
            return render(request, 'panel/info.html',
                          {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Failure",
                           'msg': "Remove from Cart Failed, Book Not Exists!", 'orders': orders, 'orderSum': len(orders), 'sales': sales, 'saleSum': len(sales), 'bookSum': len(sale_books), 'balance': balance})
        Car.objects.get(item=delete, user=useroutlet).delete()
        ids = Car.objects.filter(user=useroutlet)
        idset = []
        for idi in ids:
            idset.append(idi.item)
        books = Book.objects.filter(id__in=idset, isDelete=False).order_by('id')

        paginator = Paginator(books, 3)  # Show 2 contacts per page

        page = request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            books = paginator.page(paginator.num_pages)

        return render(request, 'panel/info.html',
                      {'username': request.user.username, 'books': books,
                       'TYPE': "Success", 'msg': "Remove from Cart Successfully!", 'orders': orders, 'orderSum': len(orders), 'sales': sales, 'saleSum': len(sales), 'bookSum': len(sale_books), 'balance': balance})

    if purchased:
        return render(request, 'panel/info.html', {'username': request.user.username, 'books': books, 'TYPE': "Success", 'msg': "Purchased Successfully!", 'orders': orders, 'orderSum': len(orders), 'sales': sales, 'saleSum': len(sales), 'bookSum': len(sale_books), 'balance': balance})
    else:
        return render(request, 'panel/info.html', {'username': request.user.username, 'books': books, 'orders': orders, 'orderSum': len(orders), 'sales': sales, 'saleSum': len(sales), 'bookSum': len(sale_books), 'balance': balance})
