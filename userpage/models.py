from django.db import models
from adminpage.models import UsersModel
from django.core.exceptions import ValidationError

# Create your models here.

def validate_tell_num(tell):
    if( "+998" or tell.range == 9) in tell:
        return tell
    else:
        raise ValidationError("Telefon raqami +998 bilan boshlanishi kerak")

class ClientModel(models.Model):
    user = models.ForeignKey(UsersModel, blank=True,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    surename = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    tell = models.CharField( blank=True,null=True,max_length=13,default='+998', validators=[validate_tell_num])
    market_name = models.CharField(blank=True, null=True, default="market", max_length=25)
    date = models.DateTimeField(blank=True,null=True, auto_now_add=True)
    descriptions = models.TextField(blank=True,null=True)
    class Meta:
        db_table ="ClientModel"

    def __str__(self) -> str:
        return self.name
    
class Unit(models.Model):
    user = models.ForeignKey(UsersModel,blank=True,null=True,on_delete=models.CASCADE)
    unit_name = models.CharField(blank=True, null=True, max_length=15)
    
    class Meta:
        db_table= "Units"
    
    def __str__(self) -> str:
        return self.unit_name


class Product(models.Model):
    user = models.ForeignKey(UsersModel,blank=True,null=True,on_delete=models.CASCADE)
    product = models.CharField(blank=True, null=True, max_length=15)
    
    class Meta:
        db_table= "Product"
    
    def __str__(self) -> str:
        return self.product
    

class ProductModel(models.Model):
    unit = models.ForeignKey(Unit, blank=True,null=True, default='birliklar', on_delete=models.CASCADE)
    client = models.ForeignKey(ClientModel, blank=True,null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UsersModel,blank=True,null=True,on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product,max_length=25, on_delete=models.CASCADE, null=True)
    price = models.FloatField(default=0)
    date = models.DateField(null=True)
    sum_price = models.FloatField(blank=True,null=True, default=0)
    quantity_product = models.FloatField()
    to_pay = models.FloatField(blank=True, null=True, default=0)
    debt = models.FloatField(blank=True, null=True, default=0)

    
    class Meta:
        db_table ="ProductModel"

    def __str__(self) -> str:
        return self.client.name
    

