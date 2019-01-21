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


# 最优
@login_required
def addcar(request):
    user = request.user
    book_id = request.POST.get('id')
    check = Car.objects.filter(item=book_id, user=user)
    if check:
        return HttpResponse('Already Add This Book!')
    Car.objects.create(item=book_id, user=user)
    return HttpResponse('Add Successfully!')


# 最优
@login_required
def removecar(request):
    user = request.user
    book_id = request.POST.get('id')
    check = Car.objects.filter(item=book_id, user=user)
    if check:
        return HttpResponse('Remove Successfully!')
