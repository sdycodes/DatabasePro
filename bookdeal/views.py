from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from bookdeal.models import *
# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    if request.method == 'POST':
        # get the information
        name = request.POST.get('name')
        passwd1 = request.POST.get('password1')
        passwd2 = request.POST.get('password2')
        typ = request.POST.get('type')
        # check if they are legal
        if name == "" or passwd1 == "" or typ == "":
            return render(request, 'result.html', {'func': 'signup', 'res': 'cannot be null'})
        if passwd1 != passwd2:
            return render(request, 'result.html', {'func': 'signup', 'res': 'passwd not equal'})
        res = User.objects.filter(name=name)
        if res:
            return render(request, 'result.html', {'func': 'signup', 'res': 'name already exists!'})
        # sign up
        if typ == 'n':
            Normal.objects.create(name=name, passwd=passwd1)
        else:
            Retailer.objects.create(name=name, passwd=passwd1)
            return render(request, 'result.html', {'func': 'signup', 'res': 'success'})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        normal_user = Normal.objects.filter(name=name)
        if normal_user:
            if normal_user[0].passwd == passwd:
                return render(request, 'result.html', {'func': 'signin', 'res': normal_user[0].name})
            else:
                return render(request, 'result.html', {'func': 'sign', 'res': 'wrong password!!'})
        else:
            retail_user = Retailer.objects.filter(name=name)
            if retail_user:
                if retail_user[0].passwd == passwd:
                    return render(request, 'result.html', {'func': 'signin', 'res': retail_user[0].name})
                else:
                    return render(request, 'result.html', {'func': 'sign', 'res': 'wrong password!!'})
            else:
                return render(request, 'result.html', {'func': 'signin', 'res': 'not exists!'})


def add_book(request):
    pass


def delete_book(request):
    pass

def search_book(request):
    pass

