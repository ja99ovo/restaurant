from django.db import models

class Boisson(models.Model):

    name=models.CharField(max_length=20)
    prix=models.IntegerField()

class Table(models.Model):
    name=models.CharField(max_length=20,null=True)


class Order(models.Model):

    table=models.ForeignKey(Table,on_delete=models.SET_NULL, related_name='orders',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    adults = models.IntegerField(default=0)  # 成人数量
    kids = models.IntegerField(default=0)    # 大孩子数量
    toddlers = models.IntegerField(default=0) # 小孩子数量
    status = models.CharField(max_length=50,default='Active')
    prix=models.IntegerField(null=True)

class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    boisson = models.ForeignKey(Boisson,on_delete=models.CASCADE)
    quantity = models.IntegerField()

