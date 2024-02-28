from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UsersChangeForm, UsersCreationForm
from .models import UsersModel
from django.urls import reverse
from django.utils.html import format_html

# Register your models here.

class UsersAdmin(UserAdmin):
    add_form = UsersCreationForm
    form = UsersChangeForm
    model = UsersModel()
    def change_password_link(self, obj):
        url = reverse('admin_change_user_password', args=[obj.pk])
        return format_html('<a href="{}">Parolni o\'zgartirish</a>', url)
    change_password_link.short_description = 'Parolni o\'zgartirish'
    
    list_display = ['username','first_name','last_name','email','address','tell','is_staff','change_password_link']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address','tell',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('address','tell',)}),
    )




admin.site.register(UsersModel, UsersAdmin),
