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
from bookdeal.tests import *
# Create your views here.


def report(request):
    if request.method == 'GET':
        return render(request, 'test/report.html')
    if request.method == 'POST':
        user_name = request.user.name
        info = request.POST.get('info')
        user = Normal.objects.filter(user_name=user_name)
        trans_id = request.POST.get('id')
        check = Order.objects.filter(id=trans_id, buyer=user)
        if check:
            Report.objects.create(reporter=user, trans=Order, info=info)
            HttpResponse('report waiting for process')
        else:
            HttpResponse('you cannot report other transaction')


def correct(request):
    if request.method == 'GET':
        return render(request, 'test/correct.html')
    if request.method == 'POST':
        corrector = request.user
        info = request.POST.get('info')
        Correct.objects.create(corrector=corrector, info=info)
        return HttpResponse('corrections has been submitted')


def get_recommend(request):
    if request.method == 'GET':
        user = request.user
        normal = Normal.objects.get(user=user)
        if normal.grade and normal.dept:
            res = Rlist.objects.filter(grade=normal.grade, dept=normal.dept)
            if res:
                return HttpResponse(res[0])
            else:
                return HttpResponse('we have not build the recommend yet')
        else:
            return HttpResponse('please give us more your info')


def handle_report(request):
    if request.method == 'GET':
        return render('test/handle_report.html')
    if request.method == 'POST':
        punish = request.POST.get('punish')
        name = request.POST.get('name')
        punished = User.objects.filter(username=name)
        if punished:
            punished = punished[0]
        if punish <= 0.5:
            punished.isDelete = True
        else:
            punished.credit = punish
        return render('result.html', {'func': 'handle_request', 'res': 'successful'})


def handle_correct(request):
    if request.method == 'GET':
        return render('test/handle_correct.html')
    if request.method == 'POST':
        dept = request.POST.get('dept')
        grade = request.POST.get('grade')
        names = request.POST.get('names')
        res = Rlist.objects.filter(dept=dept, grade=grade)
        if res:
            res = res[0]
        res.objects.update(names=names)
        return HttpResponse('success')


def front(request):
    return render(request, 'front/index.html')


def panel(request):
    balance, saleSum = getBalance(request)
    if request.user.username:
        return render(request, 'panel/index.html', {'username': request.user.username, 'TYPE': "Success", 'msg': "Welcome Back!", 'balance': balance, 'saleSum': saleSum})
    else:
        return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "Please Login First!"})
