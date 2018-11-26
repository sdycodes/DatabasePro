from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
from bookdeal.views import *


def signup(request):
    # 注册用户
    if request.method == 'GET':
        return render(request, 'panel/adduser.html')
    if request.method == 'POST':
        # get the information
        name = request.POST.get('name')
        passwd1 = request.POST.get('password1')
        passwd2 = request.POST.get('password2')
        typ = request.POST.get('typ')
        # check if they are legal
        res = User.objects.filter(username=name)
        if res:
            return render(request, 'panel/index.html',
                          {'TYPE': "Failure", 'msg': 'User ' + name + ' Already Exists!',
                           "username": request.user.username})
        # sign up
        if typ == "a":
            Retailer.objects.create_user(username=name, password=passwd1)
        elif typ=="n":
            Normal.objects.create_user(username=name, password=passwd1)
        else:
            Admin.objects.create_user(username=name, password=passwd1)
        return render(request, 'panel/index.html',
                      {'TYPE': "Success", 'msg': 'User ' + name + ' Successfully Added!',
                       "username": request.user.username})


def login(request):
    # 登陆
    if request.method == 'GET':
        request.session.flush()
        return render(request, 'panel/login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        rem = request.POST.get('remember')
        if rem is not "true":
            request.session.set_expiry(0)
        user = auth.authenticate(username=name, password=passwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            if Admin.objects.filter(username=request.user.username):
                reports = Report.objects.filter()
                corrections = Correct.objects.filter()
                return render(request, 'panel/index_admin.html', {'username': request.user.username, 'res': name,
                                                                  'reports': reports, 'corrections': corrections})
            else:
                return render(request, 'panel/index.html', {'username': request.user.username, 'res': name})
        else:
            return render(request, 'panel/login.html', {'username': '', 'TYPE': 'Failure',
                                                        'msg': "Invalid Password or Username!"})


def settings(request):
    # 修改用户信息
    balance, saleSum = getBalance(request)
    if request.method == 'GET':
        return render(request, 'panel/settings.html', {'username': request.user.username, 'user': request.user, 'balance': balance, 'saleSum': saleSum})
    if request.method == 'POST':
        # get the information
        name = request.POST.get('name')
        res = User.objects.filter(username=name)
        if res:
            opasswd = request.POST.get('oldpassword')
            user = auth.authenticate(username=name, password=opasswd)
            if user is not None and user.is_active:
                current = res[0]
                passwd = request.POST.get('password1')
                current.set_password(passwd)
                return render(request, 'panel/index.html',
                              {'TYPE': "Success", 'msg': 'Successfully Modified Password for User ' + name + '!',
                               "username": request.user.username, 'balance': balance, 'saleSum': saleSum})
        else:
            return render(request, 'panel/index.html',
                          {'TYPE': "Failure", 'msg': 'User ' + name + ' Password Mismatch!',
                           "username": request.user.username, 'balance': balance, 'saleSum': saleSum})
