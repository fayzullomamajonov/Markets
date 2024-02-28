from django.forms import ModelForm,TextInput
from django import forms
from .models import ClientModel,ProductModel, Unit,Product
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from adminpage.models import UsersModel
# from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class AddUnitForm(forms.ModelForm):
    class Meta:
        model= Unit
        fields = ['unit_name']
        labels = {
            'unit_name':_('O`lchov birligi'),
        }
    def __init__(self, *args, **kwargs):
        super(AddUnitForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=['product']
        labels = {
            'product':_('Mahsulot nomi'),
        }
    def __init__(self, *args, **kwargs):
        super(AddProductForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})



class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['name','surename','address','tell','market_name','descriptions',]
        labels ={
            'name':_('Ism'),
            'surename':_('Familiya'),
            'address':_('Manzil'),
            'tell':_('Telefon raqam'),
            'market_name':_('Dokon nomi'),
            'descriptions':_('Izoh qoldirish'),
        }
        widgets = {
            'descriptions':TextInput(attrs={
                'style': 'height:50px;' ,
                'placeholder':'Izoh qoldirish',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})


class ClientChangeForm(UserChangeForm):
    class Meta:
        model = ClientModel
        fields = ('name', 'surename','address','tell','market_name','descriptions')
        labels ={
            'name':_('Ism'),
            'surename':_('Familiya'),
            'address':_('Manzil'),
            'tell':_('Telefon raqam'),
            'market_name':_('Dokon nomi'),
            'descriptions':_('Izoh qoldirish'),
        }
        widgets = {
            'descriptions':TextInput(attrs={
                'style': 'height:50px;' ,
                'placeholder':'Izoh qoldirish',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})



class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['date','product_name','quantity_product','unit','price','to_pay', ]
        labels ={
            'date':_('Mahsulot yetkazilgan sana'),
            'product_name':_('Mahsulot nomi'),
            'quantity_product':_('Mahsulot soni (miqdori)'),
            'unit':_('O`lchov birligi'),
            'price':_('Mahsulot narxi (1 dona yoki 1 kg)'),
            'to_pay':_('To`landi (uzs)'),
        }
        widgets = {
            'date':forms.DateInput(attrs={'type':'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.filter(Q(user=user) | Q(user__isnull =True))
        self.fields['product_name'].queryset = Product.objects.filter(user=user)

        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})

class ProductChangeForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['date','product_name','quantity_product','unit','price','to_pay', ]
        labels ={
            'date':_('Mahsulot yetkazilgan sana'),
            'product_name':_('Mahsulot nomi'),
            'quantity_product':_('Mahsulot soni (miqdori)'),
            'unit':_('O`lchov birligi'),
            'price':_('Mahsulot narxi (1 dona yoki 1 kg)'),
            'to_pay':'To`landi (uzs)',
        }
        widgets = {
            'date':forms.DateInput(attrs={'type':'date'})
        }

    def __init__(self,user, *args, **kwargs):
        super(ProductChangeForm, self).__init__(*args, **kwargs)
        self.fields['unit'].queryset = Unit.objects.filter(Q(user=user) | Q(user__isnull =True))
        self.fields['product_name'].queryset = Product.objects.filter(user=user)
        for key, field in self.fields.items():
            field.widget.attrs.update({"class": "input input--text"})

class PasswordChangeingForm(PasswordChangeForm):
    class Meta:
        model = UsersModel
        fields = ['old_password', 'new_password1', 'new_password2']
        labels = {
            'old_password':_('Eski parol kiriting'),
            'new_password1':_('Yangi parol kiriting'),
            'new_password2':_('Yangi parolni qayta kiriting'),
        }




# class DateFilterForm(forms.Form):
#     start_date = forms.DateField(
#         label='Kundan:',
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         input_formats=['%Y-%m-%d']
#     )
#     end_date = forms.DateField(
#         label='Kungacha:',
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         input_formats=['%Y-%m-%d']
#     )