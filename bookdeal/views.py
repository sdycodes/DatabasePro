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


def list_myissue(request):
    if request.method == 'GET':
        balance, saleSum = getBalance(request)
        name=request.user.username
        try:
            useroutlet = Normal.objects.get(username=name)
        except Normal.DoesNotExist:
            try:
                useroutlet = Retailer.objects.get(username=name)
                sale_books = Book.objects.filter(owner=useroutlet)
                sales = Order.objects.filter(book_id__in=sale_books)
                orders = []
                sale_books = Book.objects.filter(owner=useroutlet)
                books = Order.objects.filter(book_id__in=sale_books)
                idset = []
                for idi in books:
                    idset.append(idi.buyer)
                buyers = User.objects.filter(username__in=idset)
                issues = Report.objects.filter(reporter__in=buyers)

                books = Order.objects.filter(buyer=useroutlet)
                idset = []
                for idi in books:
                    idset.append(idi.book_id.owner)
                print(idset)
                owners = User.objects.filter(username__in=idset)
                print(owners)
                issues = issues | Report.objects.filter(reporter__in=owners)
                reports = Report.objects.filter(reporter=request.user).order_by('id')
                return render(request, 'panel/list_myissue.html',
                              {'username': request.user.username, 'retail': True, 'orders': orders, 'issues': issues,
                               'reports': reports, 'orderSum': len(orders), 'sales': sales, 'saleSum': saleSum, 'balance': balance})
            except Retailer.DoesNotExist:
                return render(request, 'panel/index.html',
                              {'username': request.user.username, 'TYPE': "Warning",
                               'msg': "Please Login First!"})
        sale_books = Book.objects.filter(owner=useroutlet)
        books = Order.objects.filter(book_id__in=sale_books)
        idset = []
        for idi in books:
            idset.append(idi.buyer)
        buyers = User.objects.filter(username__in=idset)
        issues = Report.objects.filter(reporter__in=buyers)

        books = Order.objects.filter(buyer=useroutlet)
        idset = []
        for idi in books:
            idset.append(idi.book_id.owner)
        print(idset)
        owners = User.objects.filter(username__in=idset)
        print(owners)
        issues = issues | Report.objects.filter(reporter__in=owners)
        report_id = request.GET.get('del')
        if report_id is not None:
            tar = Report.objects.filter(id=report_id, reporter=request.user).order_by('id')
            if tar:
                Report.objects.delete(id=report_id, reporter=request.user)
                reports = Report.objects.filter(id=report_id, reporter=request.user).order_by('id')
                return render(request, 'panel/list_myissue.html', {'username': request.user.username, 'reports': reports, 'issues': issues,
                                                                  'TYPE': "Success",
                                                                  'msg': "delete successfully", 'balance': balance, 'saleSum': saleSum})
            reports = Report.objects.filter(reporter=request.user).order_by('id')
            if reports:
                return render(request, 'panel/list_myissue.html', {'username': request.user.username, 'TYPE': "Failure",
                                                                  'msg': "Error Occurred!", 'reports': reports, 'issues': issues, 'balance': balance, 'saleSum': saleSum})
            else:
                return render(request, 'panel/list_myissue.html', {'username': request.user.username, 'TYPE': "Warning",
                                                                  'msg': "No Reports Available Yet!", 'balance': balance, 'saleSum': saleSum})
        else:
            reports = Report.objects.filter(reporter=request.user).order_by('id')
            if reports:
                return render(request, 'panel/list_myissue.html', {'username': request.user.username, 'reports': reports, 'issues': issues, 'issues': issues, 'balance': balance, 'saleSum': saleSum})
            else:
                return render(request, 'panel/list_myissue.html', {'username': request.user.username, 'TYPE': "Warning",
                                                                  'msg': "No Reports Available Yet!", 'balance': balance, 'issues': issues, 'saleSum': saleSum})


def issue(request, report_id):
    report = Report.objects.filter(id=report_id)
    if report:
        report = report[0]
        if report.trans.buyer == request.user.username:
            return render(request, 'panel/report.html',
                      {'username': request.user.username, 'report': report, 'retail': "Buyer"})
        elif report.trans.book_id.owner.username == request.user.username:
            return render(request, 'panel/report.html',
                          {'username': request.user.username, 'report': report, 'retail': "Seller"})
        else:
            return render(request, 'panel/report.html',
                          {'username': request.user.username, 'report': report, 'retail': "Third Party"})
    else:
        return render(request, 'panel/report.html',
                      {'username': request.user.username, 'TYPE': "Failure",
                       'msg': "Unable to obtain report information!"})


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
    if request.user.username and Admin.objects.filter(username=request.user.username):
        reports = Report.objects.all()
        corrections = Correct.objects.all()
        lists = Rlist.objects.all()
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'lists': lists,
                                                              'reports': reports, 'corrections': corrections})
    elif request.user.username:
        return render(request, 'panel/index.html', {'username': request.user.username, 'TYPE': "Success", 'msg': "Welcome Back!", 'balance': balance, 'saleSum': saleSum})
    else:
        return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "Please Login First!"})


def detail_report(request):
    q = ""
    p = ""
    d = ""
    try:
        q = request.GET['repo_id']
    except:
        pass
    try:
        p = request.GET['p']
    except:
        pass
    try:
        d = request.GET['d']
    except:
        pass

    reports = Report.objects.all()
    corrections = Correct.objects.all()
    lists = Rlist.objects.all()
    if q and p == "":
        detail = Report.objects.get(id=q)
        reported = detail.trans.book_id.owner.username
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'detail': detail, 'lists':lists,
                                                          'reported': reported, 'reports': reports, 'corrections': corrections})
    if p != "":
        print(p)
        res = Normal.objects.filter(username=p)
        if res:
            user = res[0]
        else:
            user = Retailer.objects.get(username=p)
        if user.credit > 1:
            user.credit -= 1
        user.save()
        detail = Report.objects.get(id=q)
        reported = detail.trans.book_id.owner.username
        msg = "punish" + user.username
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'detail': detail, 'lists':lists,
                                                          'reported': reported, 'reports': reports, 'msg': msg,
                                                          'TYPE': "Success", 'corrections': corrections})
    if d != "":
        repo = Report.objects.get(id=d)
        repo.isFinish = True
        repo.save()
        msg = "Finish a report!"
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'lists':lists,
                                                          'reports': reports, 'msg': msg,
                                                          'TYPE': "Success", 'corrections': corrections})


def addrlist(request):
    reports = Report.objects.all()
    corrections = Correct.objects.all()
    books = Book.objects.all()
    lists = Rlist.objects.all()
    if request.method == 'GET':
        lg = request.GET.get('lg')
        ld = request.GET.get('ld')
        res = Rlist.objects.filter(dept=ld, grade=lg)
        dept = ""
        grade = ""
        names = ""
        if res:
            res = res[0]
            dept = res.dept
            grade = res.grade
            names = res.names
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'add':True, 'books':books,
                                                          'reports': reports, 'corrections': corrections, 'res': res,
                                                          'lists': lists, 'dept': dept, 'grade': grade, 'names': names})
    if request.method == 'POST':
        dept = request.POST.get('dept')
        grade = request.POST.get('grade')
        names = request.POST.get('names')
        res = Rlist.objects.filter(dept=dept, grade=grade)
        if res:
            res = res[0]
            res.names = names
            res.save()
        else:
            Rlist.objects.create(dept=dept, grade=grade, names=names)
        return render(request, 'panel/index_admin.html', {'username': request.user.username,
                                                          'reports': reports, 'corrections': corrections,'lists': lists,
                                                          'msg': "Success add!", 'TYPE': "Success"})
