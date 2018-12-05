from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
from bookdeal.views import *
from bookdeal.functions_user import *
from bookdeal.functions_car import *
from bookdeal.functions_book import *
from django.contrib.auth.decorators import login_required


def getBalance():
    sales = len(Order.objects.all())
    balance = Order.objects.select_related('book_id').aggregate(Sum('book_id__price'))
    balance = balance['book_id__price__sum'] if balance['book_id__price__sum'] else 0
    return balance, sales


# 三次 一次确定用户 一次确定购物车 一次确定书籍信息
@login_required
def purchase(request):
    user = request.user
    if request.method == 'POST':
        purchased = False
        checks = request.POST.get('checkRow')
        if checks:
            buyer = user.username
            for id in checks:
                book = Book.objects.filter(id=id, isDelete=False).order_by('id')
                if book:
                    book = book[0]
                book.isDelete = False
                book.save()
                Order.objects.create(buyer=buyer, book_id=book, isFinish=False)
                useroutlet = user.normal
                Car.objects.get(item=id, user=useroutlet).delete()
                purchased = True

        name = user.username
        # try:
        #     useroutlet = Normal.objects.get(username=name)
        # except Normal.DoesNotExist:
        #     try:
        #         useroutlet = Retailer.objects.get(username=name)
        #         return render(request, 'panel/info.html', {'username': request.user.username})
        #     except Retailer.DoesNotExist:
        #         return render(request, 'panel/index.html',
        #                       {'username': request.user.username, 'TYPE': "Warning",
        #                        'msg': "Please Login First!"})
        if not user or user.first_name == 'g':
            return render(request, 'panel/index.html',
                                    {'username': name, 'TYPE': "Warning",
                                     'msg': "Please Login as a right identity!"})
        if user.first_name == 'a':
            return render(request, 'panel/info.html', {'username':name})
        useroutlet = user.normal
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


# tql  貌似所有的交易全部在一个函数里实现了
# 只会查一次  为了显示本次交易有多少次举报
# 关键是以前代码风格不好 大量的重复
@login_required
def order(request, order_id, retail):
    order = Order.objects.get(id=order_id)
    balance, saleSum = getBalance()
    if request.method == 'POST':
        report = request.POST.get('report')
        comment = request.POST.get('comment')
        # 用户提交了一个举报
        if report:
            # 如果有举报详细内容 创建这条举报
            if comment:
                Report.objects.create(reporter=request.user, trans=order, isFinish=False, info=comment)
                Type = "Success"
                msg = "Successfully Submit Report Information!"
            else:
                Type = "Failure"
                msg = "Failed due to Empty Information!"

            reports = Report.objects.filter(trans=order)
            return render(request, 'panel/order.html',
                            {'username': request.user.username, 'TYPE': Type,
                               'msg': msg, 'order': order, 'retail': retail,
                               'balance': balance, 'saleSum': saleSum, 'reports': reports, 'reportSum': len(reports)})
        # 处理评分
        else:
            star = request.POST.get('star')
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

    if not order:
        return render(request, 'panel/order.html',
                        {'username': request.user.username, 'TYPE': "Failure",
                                           'msg': "Unable to obtain order information!"})
    reports = Report.objects.filter(trans=order)
    return render(request, 'panel/order.html',
                            {'username': request.user.username, 'order': order,
                                    'retail': retail, 'balance': balance, 'saleSum': saleSum,
                                    'reports': reports, 'reportSum': len(reports)})
