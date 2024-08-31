from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class pro(models.Model):
    CAT=((1,'forest'),(2,'Art'),(3,'people'))
    name=models.CharField(max_length=50,verbose_name="Services Name")
    price=models.FloatField()
    description=models.CharField(max_length=100,verbose_name="Services Details")
    Categories=models.IntegerField(verbose_name="Category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    portrait=models.ImageField(upload_to='image')
    summary=models.CharField(max_length=1000,verbose_name="Service Summary")
    writer=models.CharField(max_length=200,verbose_name="writer name")
    subj=models.CharField(max_length=200,verbose_name=" writer subj")

class cont(models.Model):
    customer_name=models.CharField(max_length=40)
    customer_email=models.CharField(max_length=40)
    customer_concern=models.CharField(max_length=40)
    customer_message=models.CharField(max_length=100)

class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(pro,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)


class order(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(pro,on_delete=models.CASCADE,db_column="pid")
    qty=models.IntegerField(default=1)
    order_id=models.CharField(max_length=50)