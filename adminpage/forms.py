from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UsersModel, AdminMessageModel
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _


class UsersCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
    
    class Meta(UserCreationForm):
        model = UsersModel
        fields = [ 'first_name', 'last_name','address','tell','username','password1','password2' ]
        labels = {
            'first_name':_("Ism"),
            'last_name': _("Familiya"),
            'username':_("Login"),
            'address':_('Manzil'),
            'tell':_('Telefon raqam'),

            # 'is_blocked':_('Foydalanuvchini blocklash')
        }
        help_texts = {
            'username': None,
            'email':None,
        }

            
class UsersChangeForm(UserChangeForm):
    class Meta:
        model = UsersModel
        fields = ( 'first_name', 'last_name','username','address','tell','is_blocked',)
        labels = {
            'first_name':_("Ism"),
            'last_name': _("Familiya"),
            'username':_("Login"),
            'address':_('Manzil'),
            'tell':_('Telefon raqam'),
            'is_blocked':_('Foydalanuvchini blocklash'),
        }
        help_texts = {
            'username':None,
        }
        
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})

class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = AdminMessageModel
        fields = ('message_title','message_description')
        labels = {
            'message_title':_('Xabar mavzusi'),
            'message_description':_('Xabar matni'),
        }
    def __init__(self, *args, **kwargs):
        super(AdminMessageForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})




