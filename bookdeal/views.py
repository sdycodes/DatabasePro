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
        name = request.POST.get('name')
        passwd = request.POST.get('password')
        reg = Normal.objects.create(name=name, passwd=passwd)
        return render(request, 'result.html', {'func': 'signup', 'res': reg})
