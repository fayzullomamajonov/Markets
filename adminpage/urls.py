from django.urls import path
from .views import *

urlpatterns = [
    path('user/list',users_list_view, name='users_list'),
    # path('registretions/users/',SignupUsersView.as_view(), name='registrations' )
    path('registrations/',register_user,name='registrations'),
    path('', login_user, name='login'),
    path('edit/user/<int:pk>/',user_account_edit, name='account_edit' ),
    path('delete/user/<int:pk>/',user_account_delete, name='account_delete'),
    path('change/user/password/<int:user_id>/', admin_change_user_password, name='admin_change_user_password'),
    path('user/<int:pk>/',admin_userpage,name='admin_userpage'),
    # path('block_user/<int:pk>/',block_user,name='block_user'),
    path('admin_message/',admin_message,name='admin_message'),
    path('delete_message/<int:pk>/',delete_message,name='delete_message'),
]