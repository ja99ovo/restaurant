from django.db import models

class Boisson(models.Model):

    name=models.CharField(max_length=20)
    prix=models.IntegerField()

class orders(models.Model):


    created_at = models.DateTimeField(auto_now_add=True)
    adults = models.IntegerField(default=0)  # 成人数量
    kids = models.IntegerField(default=0)    # 大孩子数量
    toddlers = models.IntegerField(default=0) # 小孩子数量
    
    

class tables(models.Model):

    

    def calculate_total_price(self):
        return sum(item.price * item.quantity for item in self.orderitem_set.all())
    
    
class table_order(models.Model):
    
    related_order = models.ForeignKey(orders, on_delete=models.SET_NULL, null=True)
    related_table = models.ForeignKey(tables, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50,default='Active')


class OrderItem(models.Model):
    order = models.ForeignKey(orders, on_delete=models.CASCADE)
    boisson = models.ForeignKey(Boisson,on_delete=models.CASCADE)
    quantity = models.IntegerField()

