from django.contrib import admin
from .models import ClientModel,ProductModel,Unit,Product
# Register your models here.

admin.site.register(ClientModel)
admin.site.register(ProductModel)
admin.site.register(Unit)
admin.site.register(Product)

