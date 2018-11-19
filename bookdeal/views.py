from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
# Create your views here.


def signup(request):
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
        else:
            Normal.objects.create_user(username=name, password=passwd1)
        return render(request, 'panel/index.html',
                      {'TYPE': "Success", 'msg': 'User ' + name + ' Successfully Added!',
                       "username": request.user.username})


def signin(request):
    if request.method == 'GET':
        return render(request, 'test/signin.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        user = auth.authenticate(username=name, password=passwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            return render(request, 'test/result.html', {'func': 'signin', 'res': name})
        else:
            return render(request, 'test/result.html', {'func': 'signin', 'res': 'fail!'})


def login(request):
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
            return render(request, 'panel/index.html', {'username': request.user.username, 'res': name})
        else:
            return render(request, 'panel/login.html', {'username': '', 'TYPE': 'Failure', 'msg': "Invalid Password or Username!"})


def addbook(request):
    if request.method == 'GET':
        return render(request, 'panel/addbook.html')
    if request.method == 'POST':
        book_name = request.POST.get('name')
        info = request.POST.get('info')
        price = float(request.POST.get('price'))
        cover = request.FILES.get('cover')
        if book_name == "" or len(info) < 10 or price > 10000 or price < 0:
            return render(request, 'panel/index.html', {'TYPE':"Failure", 'msg':"addbook", "username": request.user.username})
        if cover is None or cover.name.split('.')[1].lower() not in ['jpeg', 'jpg', 'png'] or cover.size > 10000000:
            return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "illegal cover", "username":request.user.username})
        Book.objects.create(name=book_name, info=info, price=price, cover=cover, owner=request.user)
        return render(request, 'panel/index.html', {'TYPE': "Success", 'msg': 'Successfully Add Book ' + book_name + '!', "username":request.user.username})


def info(request):
    purchased = False
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
        useroutlet = Normal.objects.get(username=name)
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

    if purchased:
        return render(request, 'panel/info.html', {'username': request.user.username, 'books': books, 'TYPE': "Success", 'msg': "Purchased Successfully!"})
    else:
        return render(request, 'panel/info.html', {'username': request.user.username, 'books': books})


def purchase(request):
    if request.method == 'POST':
        purchased = False
        checks = request.POST.get('checkRow')
        if checks:
            buyer = request.user.username
            for id in checks:
                print(id)
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


def market(request):
    tar = request.POST.get('name')
    q = request.GET.get('q')
    user = request.user
    if tar is None and q is None:
        return render(request, 'panel/market.html', {'username': request.user.username})
    else:
        if q is None:
            q = tar
        books = Book.objects.filter(name__contains=q, isDelete=False).order_by('id')
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
                                   'msg': "Retailers Not Authorized to Purchase!"})
                except Retailer.DoesNotExist:
                    return render(request, 'panel/index.html',
                              {'username': request.user.username, 'TYPE': "Warning",
                               'msg': "Please Login First!"})
            check = Car.objects.filter(user=useroutlet, item=add)
            if check:
                return render(request, 'panel/market.html',
                              {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Failure",
                               'msg': "Add to Cart Failed, Book Exists!"})

            Car.objects.create(item=add, user=useroutlet)
            return render(request, 'panel/market.html',
                          {'username': request.user.username, 'books': books, 'query': q, 'TYPE': "Success", 'msg': "Add to Cart Successfully!"})

        return render(request, 'panel/market.html', {'username': request.user.username, 'books': books, 'query': q})


def list_mysell(request):
    if request.method == 'GET':
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
                                                                  'msg': "delete successfully"})
            books = Book.objects.filter(owner=request.user, isDelete=False).order_by('id')
            if books:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'TYPE': "Failure",
                                                                  'msg': "Error Occurred!", 'books': books})
            else:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'TYPE': "Warning",
                                                                  'msg': "You do not sell any single book!"})
        else:
            books = Book.objects.filter(owner=request.user, isDelete=False).order_by('id')
            if books:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'books': books})
            else:
                return render(request, 'panel/list_mysell.html', {'username': request.user.username, 'TYPE': "Warning",
                                                                  'msg': "You do not sell any single book!"})


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

# new !!

def my_car(request):
    user = request.user
    res = Car.objects.filter(owner=user)
    return render(request, 'test/list.html', {'func': 'my_car', 'res': res})


def add_car(request):
    user = request.user
    book_id = request.POST.get('id')
    check = Car.objects.filter(item=book_id, user=user)
    if check:
        return HttpResponse('already add')
    Car.objects.create(item=book_id, user=user)
    return HttpResponse('add successful')


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
    if request.user.username:
        return render(request, 'panel/index.html', {'username': request.user.username, 'TYPE': "Success", 'msg': "Welcome Back!"})
    else:
        return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "Please Login First!"})


def delete_book(request):
    if request.method == 'GET':
        return render(request, 'test/deletebook.html')
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        tar = Book.objects.filter(name=book_name, owner=request.user)
        if tar:
            book = tar[0]
            book.isDelete = True
            book.save()
            return render(request, 'test/result.html', {'func': 'delete_book', 'res': book.name})
        return render(request, 'test/result.html', {'func': 'delete_book', 'res': 'fail!'})


"""
code for test

def index(request):
    return render(request, 'test/index.html')

def add_book(request):
    if request.method == 'GET':
        return render(request, 'test/addbook.html')
    if request.method == 'POST':
        book_name = request.POST.get('name')
        info = request.POST.get('info')
        price = float(request.POST.get('price'))
        cover = request.FILES.get('cover')
        if book_name == "" or len(info) < 10 or price > 10000 or price < 0:
            return render(request, 'test/result.html', {'func': 'add_book', 'res': 'illegal input !!'})
        if cover.name.split('.')[1].lower() not in ['jpeg', 'jpg', 'png'] or cover.size > 10000000:
            return render(request, 'test/result.html', {'func': 'add_book', 'res': 'illegal cover !!'})
        Book.objects.create(name=book_name, info=info, price=price, cover=cover, owner=request.user)
        return render(request, 'test/result.html', {'func': 'add_book', 'res': 'add success!'})


def search_book(request):
    tar = request.POST.get('name')
    res = Book.objects.filter(name__contains=tar)
    return render(request, 'test/list.html', {'func': 'search_book', 'res': res})
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'test/signin.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        user = auth.authenticate(username=name, password=passwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            return render(request, 'test/result.html', {'func': 'signin', 'res': name})
        else:
            return render(request, 'test/result.html', {'func': 'signin', 'res': 'fail!'})
            
"""
