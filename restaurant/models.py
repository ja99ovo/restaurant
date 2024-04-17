from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Boisson(models.Model):
    name = models.CharField(max_length=100)
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='boissons')

    def __str__(self):
        return self.name


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

