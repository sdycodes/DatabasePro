from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Normal(User):
    credit = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    info = models.CharField(max_length=50, blank=True)
    isDelete = models.BooleanField(default=False)
    dept = models.CharField(max_length=20, blank=True)
    grade = models.IntegerField(blank=True, default=0)


class Retailer(User):
    credit = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    info = models.CharField(max_length=50, blank=True)
    isDelete = models.BooleanField(default=False)
    sale = models.IntegerField(default=0)


class Admin(models.Model):
    name = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    info = models.CharField(max_length=50, blank=True)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cover = models.ImageField(upload_to='covers')
    info = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    owner = models.ForeignKey(User,
                              related_name='owner',
                              on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)


class Rlist(models.Model):
    names = models.CharField(max_length=500)
    dept = models.CharField(max_length=50)
    grade = models.IntegerField()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.CharField(max_length=20)
    book_id = models.ForeignKey(Book, related_name='book_id', on_delete=models.CASCADE)
    brate = models.DecimalField(max_digits=1, decimal_places=1)
    srate = models.DecimalField(max_digits=1, decimal_places=1)
    date = models.DateTimeField(auto_now_add=True)
    isFinish = models.BooleanField(default=False)


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    reporter = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='reporter')
    trans = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='trans')
    info = models.CharField(max_length=1000)


class Correct(models.Model):
    id = models.AutoField(primary_key=True)
    correcter = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='correcter')
    info = models.CharField(max_length=1000)
