from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
from bookdeal.views import *


def market(request):
    tar = request.POST.get('name')
    q = request.GET.get('q')
    user = request.user
    balance, saleSum = getBalance(request)
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
            try:
                useroutlet = Normal.objects.get(username=user)
            except Normal.DoesNotExist:
                try:
                    useroutlet = Retailer.objects.get(username=user)
                    return render(request, 'panel/index.html',
                                  {'username': request.user.username, 'TYPE': "Failure",
                                   'msg': "Retailers Not Authorized to Purchase!", 'balance': balance, 'saleSum': saleSum})
                except Retailer.DoesNotExist:
                    return render(request, 'panel/index.html',
                              {'username': request.user.username, 'TYPE': "Warning",
                               'msg': "Please Login As User First!"})
            check = Car.objects.filter(user=useroutlet, item=add)
            if check:
                return render(request, 'panel/market.html',
                              {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Failure",
                               'msg': "Add to Cart Failed, Book Exists!", 'balance': balance, 'saleSum': saleSum})

            Car.objects.create(item=add, user=useroutlet)
            return render(request, 'panel/market.html',
                          {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Success", 'msg': "Add to Cart Successfully!", 'balance': balance, 'saleSum': saleSum})

        return render(request, 'panel/market.html', {'username': request.user.username, 'books': books, 'query': q, 'balance': balance, 'saleSum': saleSum})


def purchase(request):
    if request.method == 'POST':
        purchased = False
        checks = request.POST.get('checkRow')
        if checks:
            buyer = request.user.username
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
        try:
            useroutlet = Normal.objects.get(username=name)
        except Normal.DoesNotExist:
            try:
                useroutlet = Retailer.objects.get(username=name)
                return render(request, 'panel/info.html', {'username': request.user.username})
            except Retailer.DoesNotExist:
                return render(request, 'panel/index.html',
                              {'username': request.user.username, 'TYPE': "Warning",
                               'msg': "Please Login First!"})
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
            useroutlet = Normal.objects.get(username=user)
            check = Car.objects.filter(user=useroutlet, item=delete)
            if not check:
                return render(request, 'panel/info.html',
                              {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Failure",
                               'msg': "Remove from Cart Failed, Book Not Exists!"})
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
                           'TYPE': "Success", 'msg': "Remove from Cart Successfully!"})

        return render(request, 'panel/info.html', {'username': request.user.username, 'books': books})


def order(request, order_id, retail):
    if request.method == 'POST':
        report = request.POST.get('report')
        comment = request.POST.get('comment')
        if report:
            if comment:
                order = Order.objects.get(id=order_id)
                Report.objects.create(reporter=request.user, trans=order, isFinish=False, info=comment)
                balance, saleSum = getBalance(request)
                order_detail = Order.objects.get(id=order_id)
                reports = Report.objects.filter(trans=order_detail)

                return render(request, 'panel/order.html',
                              {'username': request.user.username, 'TYPE': "Success",
                                   'msg': "Successfully Submit Report Information!", 'order': order_detail, 'retail': retail,
                               'balance': balance, 'saleSum': saleSum, 'reports': reports, 'reportSum': len(reports)})
            else:
                balance, saleSum = getBalance(request)
                order_detail = Order.objects.get(id=order_id)
                reports = Report.objects.filter(trans=order_detail)
                return render(request, 'panel/order.html',
                              {'username': request.user.username, 'TYPE': "Failure",
                               'msg': "Failed due to Empty Information!", 'order': order_detail,
                               'retail': retail,
                               'balance': balance, 'saleSum': saleSum, 'reports': reports, 'reportSum': len(reports)})
        else:
            star = request.POST.get('star')
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            if order and star:
                if retail == "Retailer":
                    order.srate = star
                else:
                    order.brate = star
                order.save()
            confirm = request.POST.get('confirm')
            if order and confirm:
                order.isFinish = True
                order.save()
    balance, saleSum = getBalance(request)
    order_detail = Order.objects.get(id=order_id)

    if not order_detail:
        return render(request, 'panel/order.html',
                              {'username': request.user.username, 'TYPE': "Failure",
                               'msg': "Unable to obtain order information!"})
    reports = Report.objects.filter(trans=order_detail)
    return render(request, 'panel/order.html',
                          {'username': request.user.username, 'order': order_detail, 'retail': retail, 'balance': balance, 'saleSum': saleSum, 'reports': reports, 'reportSum': len(reports)})



def buy(request):
    if request.method == 'POST':
        buyer = request.user.name
        book_id = request.POST.get["book_id"]
        book = Book.objects.filter(id=book_id)
        if book:
            book = book[0]
        book.isDelete = False
        book.save()
        Order.objects.create(buyer=buyer, book_id=book, isFinish=False)
        return HttpResponse('successfully bought!')


def buyer_confirm(request):
    if request.method == 'GET':
        return render('test/confirm.html')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        trans = Order.objects.filter(id=order_id)
        if trans:
            trans = trans[0]
        brate = request.POST.get('rate')
        if trans.buyer == request.user.username:
            trans.brate = brate
            trans.save()
            book = trans.book_id
            seller = book.owner
            seller.credit = round((seller.credit*seller.sale + brate)/(seller.sale+1), 1)
            seller.sale += 1
            seller.save()
            if trans.srate != 0:
                trans.isFinish = True
                trans.save()
        else:
            return HttpResponse('mind on your own business!')


def seller_confirm(request):
    if request.method == 'GET':
        return render('test/confirm.html')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        trans = Order.objects.filter(id=order_id)
        if trans:
            trans = trans[0]
        srate = request.POST.get('rate')
        buyer_name = trans.buyer
        buyer = Normal.objects.filter(username=buyer_name)
        seller = trans.book_id.owner
        if seller == request.user:
            trans.srate = srate
            trans.save()
            buyer.credit = round((buyer.credit*buyer.sale + srate)/(buyer.sale+1), 1)
            buyer.sale += 1
            buyer.save()
            if trans.brate != 0:
                trans.isFinish = True
                trans.save()
            return HttpResponse('successful')
        else:
            return HttpResponse('mind on your own business!')
