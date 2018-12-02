from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from django.db.models import Sum
from bookdeal.models import *
from bookdeal.views import *
from bookdeal.functions_car import *
from bookdeal.functions_book import *
from bookdeal.functions_trans import *
from django.contrib.auth.decorators import login_required


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


@login_required
def manage(request):
    # 管理信息
    if request.user.username and Admin.objects.filter(username=request.user.username):
        if request.method == 'GET':
            book_id = request.GET.get('del')
            add_id = request.GET.get('rec')
            if book_id is not None or add_id is not None:
                if book_id is not None:
                    tar = Book.objects.filter(id=book_id).order_by('id')
                else:
                    tar = Book.objects.filter(id=add_id).order_by('id')
                if tar:
                    book = tar[0]
                    if book_id is not None:
                        book.isDelete = True
                    else:
                        book.isDelete = False
                    book.save()
                    books = Book.objects.order_by('id')
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
                    return render(request, 'panel/manage.html', {'username': request.user.username, 'books': books,
                                                                      'TYPE': "Success",
                                                                      'msg': "Modified Successfully"})
                books = Book.objects.order_by('id')
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
                if books:
                    return render(request, 'panel/manage.html',
                                  {'username': request.user.username, 'TYPE': "Failure",
                                   'msg': "Error Occurred!", 'books': books})
                else:
                    return render(request, 'panel/manage.html',
                                  {'username': request.user.username, 'TYPE': "Warning",
                                   'msg': "No Books Available on Sale!"})
            else:
                books = Book.objects.order_by('id')
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
                if books:
                    return render(request, 'panel/manage.html',
                                  {'username': request.user.username, 'books': books})
                else:
                    return render(request, 'panel/manage.html',
                                  {'username': request.user.username, 'TYPE': "Warning",
                                   'msg': "No Books Available on Sale!"})

    else:
        return render(request, 'panel/index.html',
                      {'TYPE': "Failure", 'msg': 'User ' + name + ' is not Administrator!',
                       "username": request.user.username})


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
        dept = request.POST.get('dept')
        grade = request.POST.get('grade')
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
            if dept and grade:
                Normal.objects.create_user(username=name, password=passwd1, dept=dept, grade=grade)
            elif dept:
                Normal.objects.create_user(username=name, password=passwd1, dept=dept)
            elif grade:
                Normal.objects.create_user(username=name, password=passwd1, grade=grade)
            else:
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
            return HttpResponseRedirect('/panel/')
            # if Admin.objects.filter(username=request.user.username):
            #     reports = Report.objects.all()
            #     corrections = Correct.objects.all()
            #     lists = Rlist.objects.all()
            #     return render(request, 'panel/index.html', {'username': request.user.username,
            #                                                       'reports': reports, 'corrections': corrections,
            #                                                       'lists': lists})
            # else:
            #     carnum = len(Car.objects.filter(user=user))
            #     buy = Order.objects.select_related('book_id').filter(buyer=user.username).aggregate(Sum('book_id__price'))
            #     buy = buy['book_id__price__sum'] if buy['book_id__price__sum'] else 0
            #     sale = Order.objects.select_related('book_id__owner').filter(book_id__owner__username=user.username).aggregate(Sum('book_id__price'))
            #     sale = sale['book_id__price__sum'] if sale['book_id__price__sum'] else 0
            #     names = ""
            #     nuser = Normal.objects.filter(username=request.user.username)
            #     if nuser:
            #         nuser = nuser[0]
            #         if nuser.dept and nuser.grade:
            #             rlist = Rlist.objects.filter(dept=nuser.dept, grade=nuser.grade)
            #             if rlist:
            #                 names = rlist[0].names
            #     return render(request, '/panel/index.html', {'username': request.user.username, 'res': name, 'user':user, 'carnum': carnum,
            #                                                       'sale':sale, 'buy': buy, 'total': sale+buy, 'names': names})
        else:
            return render(request, 'panel/login.html', {'username': '', 'TYPE': 'Failure',
                                                        'msg': "Invalid Password or Username!"})


@login_required
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


def login_required(request):
    return login(request)