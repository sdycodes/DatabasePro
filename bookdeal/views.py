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
from django.contrib.auth.decorators import login_required
# Create your views here.

# 优化了用户类型判断
@login_required
def list_myissue(request):
    if request.method == 'GET':
        balance, saleSum = getBalance()
        name=request.user.username
        if not request.user or request.user.first_name == 'g':
            return render(request, 'panel/index.html',
                          {'username': request.user.username, 'TYPE': "Warning",
                           'msg': "Please Login First!"})

        elif request.user.first_name == 'a':
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

        useroutlet = request.user.normal
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


@login_required
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


def front(request):
    return render(request, 'front/index.html')


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
                                                    'user': user,
                                                    'sale': sale, 'buy': 0, 'total': sale })
    # 没有用户 发出警告信息
    else:
        return render(request, 'panel/index.html', {'TYPE': "Warning", 'msg': "Please Login First!"})


# 最优
@login_required
def detail_report(request):

    q = request.GET.get('repo_id')
    p = request.GET.get('p')
    d = request.GET.get('d')
    cd = request.GET.get('cd')
    ci = request.GET.get('ci')
    reports = Report.objects.all()
    corrections = Correct.objects.all()
    lists = Rlist.objects.all()
    if q and not p:
        detail = Report.objects.get(id=q)
        reported = detail.trans.book_id.owner.username
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'detail': detail, 'lists':lists,
                                                          'reported': reported, 'reports': reports, 'corrections': corrections})
    if p:
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
    if d:
        repo = Report.objects.get(id=d)
        repo.isFinish = True
        repo.save()
        msg = "Finish a report!"
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'lists':lists,
                                                          'reports': reports, 'msg': msg,
                                                          'TYPE': "Success", 'corrections': corrections})
    if ci:
        correction = Correct.objects.get(id=ci)
        return render(request, 'panel/index_admin.html',
                      {'username': request.user.username, 'lists': lists,
                        'reports': reports, 'corrections': corrections, 'see_correct': True, 'correction':correction})
    if cd:
        correction = Correct.objects.get(id=cd)
        correction.isFinish = True
        correction.save()
        msg = "Finish a correction!"
        return render(request, 'panel/index_admin.html', {'username': request.user.username, 'lists': lists,
                                                          'reports': reports, 'msg': msg,
                                                          'TYPE': "Success", 'corrections': corrections})


# 最优
@login_required
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
        if dept and grade and names:
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
        else:
            return render(request, 'panel/index_admin.html', {'username': request.user.username,
                                                              'reports': reports, 'corrections': corrections,
                                                              'lists': lists,
                                                              'msg': "Illegal input", 'TYPE': "Failure"})

