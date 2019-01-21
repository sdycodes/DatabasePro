from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
from bookdeal.functions_user import *
from bookdeal.functions_book import *
from bookdeal.functions_car import *
from bookdeal.functions_trans import *
from bookdeal.functions_admin import *
from django.contrib.auth.decorators import login_required
from bookdeal.error_handler import *

# Create your views here.


# 最优 一次查表 计算总交易额
def getBalance():
    sales = len(Order.objects.all())
    balance = Order.objects.select_related('book_id').aggregate(Sum('book_id__price'))
    balance = balance['book_id__price__sum'] if balance['book_id__price__sum'] else 0
    return balance, sales


@login_required
def panel(request):
    balance, saleSum = getBalance()
    user = request.user
    # 如果是一个普通用户
    if user and user.first_name == 'n':
        # 填写了院系和年级 推送推荐书单
        names = ""
        if user.normal.dept and user.normal.grade:
            rlist = Rlist.objects.filter(dept=user.normal.dept, grade=user.normal.grade)
            if rlist:
                names = rlist[0].names

        # 搜索其购物车和成交额等信息
        carnum = len(Car.objects.filter(user=user))
        buy = Order.objects.select_related('book_id').filter(buyer=user.username).aggregate(Sum('book_id__price'))
        buy = buy['book_id__price__sum'] if buy['book_id__price__sum'] else 0
        sale = Order.objects.select_related('book_id__owner').filter(book_id__owner__username=user.username).aggregate(
            Sum('book_id__price'))
        sale = sale['book_id__price__sum'] if sale['book_id__price__sum'] else 0
        msg = ""

        # 如果此人传递了报错信息  将其记录下来 并返回报错成功
        correct = request.POST.get('correction')
        if request.method == 'POST' and correct:
            Correct.objects.create(corrector=user, info=correct)
            msg = 'correction has been posted'

        return render(request, 'panel/index.html',
                          {'username': user.username, 'res': user.username, 'user': user, 'carnum': carnum,
                           'sale': sale, 'buy': buy, 'total': sale - buy, 'names': names, 'balance': balance,
                           'saleSum': saleSum, 'msg': msg, 'TYPE': 'Success'})

    # 如果是管理员 向其发送报错、举报和推荐书单信息
    if user and user.first_name == 'g':
        reports = Report.objects.all()
        corrections = Correct.objects.all()
        lists = Rlist.objects.all()
        return render(request, 'panel/index_admin.html', {'username': user.username, 'lists': lists, 'balance': balance,
                           'saleSum': saleSum, 'reports': reports, 'corrections': corrections})
    # 如果是商家
    if user and user.first_name == 'a':
        sale = Order.objects.select_related('book_id__owner').filter(book_id__owner__username=user.username).aggregate(
            Sum('book_id__price'))
        sale = sale['book_id__price__sum'] if sale['book_id__price__sum'] else 0
        return render(request, 'panel/index.html', {'username': user.username, 'TYPE': "Success", 'msg': "Welcome Back!",
                                                    'balance': balance, 'saleSum': saleSum,
                                                    'user': user, 'carnum': 0,
                                                    'sale': sale, 'buy': 0, 'total': sale })
    # 没有用户 发出警告信息
    else:
        return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "Please Login First!"})




