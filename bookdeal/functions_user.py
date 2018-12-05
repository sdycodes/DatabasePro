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


# 最优 一次查表 计算总交易额
def getBalance():
    sales = len(Order.objects.all())
    balance = Order.objects.select_related('book_id').aggregate(Sum('book_id__price'))
    balance = balance['book_id__price__sum'] if balance['book_id__price__sum'] else 0
    return balance, sales


@login_required
def manage(request):
    # 管理信息
    if request.user.username and request.user.first_name == 'g':
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


# 最优  一次查表检查用户名是否可用
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
            return render(request, 'panel/adduser.html',
                          {'TYPE': "Failure", 'msg': 'User ' + name + ' Already Exists!',
                           "username": request.user.username})
        if passwd1 != passwd2:
            return render(request, 'panel/adduser.html',
                          {'TYPE': "Failure", 'msg': 'password does not match',
                           "username": request.user.username})

        # sign up
        if typ == "a":
            Retailer.objects.create_user(username=name, password=passwd1, first_name=typ)
        elif typ=="n":
            if dept and grade:
                Normal.objects.create_user(username=name, password=passwd1, dept=dept, grade=grade, first_name=typ)
            elif dept:
                Normal.objects.create_user(username=name, password=passwd1, dept=dept, first_name=typ)
            elif grade:
                Normal.objects.create_user(username=name, password=passwd1, grade=grade, first_name=typ)
            else:
                Normal.objects.create_user(username=name, password=passwd1, first_name=typ)
        else:
            Admin.objects.create_user(username=name, password=passwd1, first_name=typ)
        return render(request, 'panel/adduser.html',
                      {'TYPE': "Success", 'msg': 'User ' + name + ' Successfully Added!',
                       "username": request.user.username})


# 0次查表
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
        else:
            return render(request, 'panel/login.html', {'username': '', 'TYPE': 'Failure',
                                                        'msg': "Invalid Password or Username!"})


# 最优 一次查表 检查用户是否存在同时修改信息
@login_required
def settings(request):
    # 修改用户信息
    balance, saleSum = getBalance()
    if request.method == 'GET':
        dept = request.user.normal.dept if request.user.first_name == 'n' else ""
        grade = request.user.normal.grade if request.user.first_name == 'n' else ""
        return render(request, 'panel/settings.html', {'username': request.user.username, 'user': request.user,
                                                       'balance': balance, 'saleSum': saleSum,
                                                       'dept': dept, 'grade': grade})
    if request.method == 'POST':
        name = request.POST.get('name')
        res = User.objects.filter(username=name)
        if res:
            opasswd = request.POST.get('oldpassword')
            user = auth.authenticate(username=name, password=opasswd)
            if user is not None and user.is_active:
                current = res[0]
                passwd = request.POST.get('password1')
                current.set_password(passwd)
                dept = request.POST.get('dept')
                grade = request.POST.get('grade')
                if current.first_name == 'n' and dept:
                    current.normal.dept = dept
                if current.first_name == 'n' and grade:
                    current.normal.grade = grade
                current.normal.save()
                return render(request, 'panel/index.html',
                              {'TYPE': "Success", 'msg': 'Successfully Modified Password for User ' + name + '!',
                               "username": request.user.username, 'balance': balance, 'saleSum': saleSum})
        else:
            return render(request, 'panel/index.html',
                          {'TYPE': "Failure", 'msg': 'User ' + name + ' Password Mismatch!',
                           "username": request.user.username, 'balance': balance, 'saleSum': saleSum})


# 我也不敢大改 但至少原来判断用户的类型需要三次查找 现在一次也不需要
@login_required
def info(request):
    purchased = False
    if request.user.username and request.user.first_name == 'g':
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
    balance, saleSum = getBalance()
    orders = Order.objects.filter(buyer=name)
    if not request.user or request.user.first_name == 'g':
        return render(request, 'panel/index.html',
                      {'username': request.user.username, 'TYPE': "Warning",
                       'msg': "Please Login First!"})
    elif request.user.first_name == 'a':

        sale_books = Book.objects.filter(owner=useroutlet)
        sales = Order.objects.filter(book_id__in=sale_books)
        return render(request, 'panel/info.html',
                      {'username': request.user.username, 'retail': True, 'orders': orders, 'orderSum': len(orders),
                       'sales': sales, 'saleSum': saleSum, 'balance': balance})

    useroutlet = request.user.normal
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


def login_required(request):
    return login(request)
