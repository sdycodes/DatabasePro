from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.views import generic
from django.contrib import auth
from bookdeal.models import *
# Create your views here.


def index(request):
    return render(request, 'test/index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'test/signup.html')
    if request.method == 'POST':
        # get the information
        name = request.POST.get('name')
        passwd1 = request.POST.get('password1')
        passwd2 = request.POST.get('password2')
        typ = request.POST.get('type')
        # check if they are legal
        if name == "" or passwd1 == "" or typ == "":
            return render(request, 'test/result.html', {'func': 'signup', 'res': 'cannot be null'})
        if passwd1 != passwd2:
            return render(request, 'test/result.html', {'func': 'signup', 'res': 'passwd not equal'})
        res = User.objects.filter(username=name)
        if res:
            return render(request, 'test/result.html', {'func': 'signup', 'res': 'name already exists!'})
        # sign up
        if typ == 'n':
            Normal.objects.create_user(username=name, password=passwd1)
        else:
            Retailer.objects.create_user(username=name, password=passwd1)
        return render(request, 'test/result.html', {'func': 'signup', 'res': 'success'})


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
        return render(request, 'panel/login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        user = auth.authenticate(username=name, password=passwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            return render(request, 'test/result.html', {'func': 'signin', 'res': name})
        else:
            return render(request, 'panel/login.html', {'func': 'signin', 'res': 'fail!'})



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


def market(request):
    return render(request, 'panel/market.html')


def list_mysell(request):
    books = Book.objects.filter(owner=request.user, isDelete=False)
    if books:
        return render(request, 'test/list.html', {'books': books})
    return render(request, 'test/result.html', {'func': 'list_mysell', 'res': 'None!'})


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


# new !!!

def search_book(request):
    tar = request.POST.get('name')
    res = Book.objects.filter(name__contains=tar)
    return render(request, 'test/list.html', {'func': 'search_book', 'res': res})


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
    return render(request, 'panel/index.html')
