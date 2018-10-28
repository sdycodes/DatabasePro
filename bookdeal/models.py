from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=20)
    cred = models.DecimalField(max_digits=1,
                               decimal_places=1,
                               default=5.0)
    info = models.CharField(max_length=50, blank=True)


class Normal(User):
    dept = models.CharField(max_length=20, blank=True)
    grade = models.IntegerField(blank=True)


class Retailer(User):
    sale = models.IntegerField()


class Admin(models.Model):
    name = models.CharField(max_length=20)
    passwd = models.CharField(max_length=20)
    info = models.CharField(max_length=50, blank=True)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    cover = models.ImageField()
    info = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    owner = models.ForeignKey(User,
                              related_name='owner',
                              on_delete=models.CASCADE)


class Rlist(models.Model):
    names = models.CharField(max_length=500)
    dept = models.CharField(max_length=50)
    grade = models.IntegerField()


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.CharField(max_length=20)
    seller = models.CharField(max_length=20)
    book = models.IntegerField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
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
