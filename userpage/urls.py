from django.urls import path
from .views import *

urlpatterns = [
    path('statistics/<int:pk>/',statistics_view,name='statistics'),
    path('userpages/<int:pk>/',homepage_view, name='userpages'),
    path('add_client/', client_add, name='add_client'),
    path('client/<int:pk>/', clientpage, name='clientpage'),
    path('to/sell/<int:pk>/',to_sell_page, name='to_sell_page'),
    path('payment/<int:pk>/', payment_view, name='payment'),
    path('peyment_amount/<int:pk>/', peyment_amount, name='peyment_amount'),
    path('client_edit/<int:pk>/', client_edit, name='client_edit'),
    path('client_delete/<int:pk>/', client_delete, name='client_delete'),
    path('product_delete/<int:pk>/', product_delete, name='product_delete'),
    path('product_edit/<int:pk>/', product_edit, name='product_edit'),
    path('change_password/', view=PasswordChangeView.as_view(template_name='userpage/password_change.html'),
        name='change_password'),
    path('success_password/',password_success,name='success_password'),
    path('add/unit/',add_unit,name='add_unit'),
    path('unit/delete/<int:pk>/',unit_delete,name='unit_delete'),
    path('add/products/',add_product,name='add_product'),
    path('products/delete/<int:pk>/',products_delete,name='products_delete'),
    path('message_p/<int:pk>/',message_page,name='message_page'),


]