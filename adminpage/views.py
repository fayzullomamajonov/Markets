from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import user_passes_test
from .forms import UsersCreationForm,UsersChangeForm,AdminMessageForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UsersModel,AdminMessageModel
from django.utils.translation import gettext_lazy as _
from django.core.paginator import Paginator
from datetime import datetime, timedelta

# from .decorators import check_blocked
from django.db.models import Count
from django.db.models import Q

# Create your views here.

def users_list_view(request):
    if 'search' in request.GET:
        search = request.GET['search']
        user_list = UsersModel.objects.filter(
            Q(first_name__icontains=search)|
            Q(last_name__icontains=search)|
            Q(address__icontains=search)
            
        )
    else:
        user_list = UsersModel.objects.order_by('-date_joined')
    # user_list = UsersModel.objects.order_by('-date_joined')
    paginator = Paginator(user_list, 10)

    page = request.GET.get("page")
    user_list = paginator.get_page(page)
    context = {
        'user_list':user_list,
        # 'data':data,
    }
    return render(request,'adminpage/users_list.html',context)


def admin_userpage(request, pk):
    user_page = get_object_or_404(UsersModel, id=pk)
    context = {
        'user_page':user_page,
    }
    return render(request,'adminpage/admin_userpage.html',context)



def register_user(request):
    form = UsersCreationForm()
    for f in form:
        if f.label == "Password":
            f.label = "Parol"
        elif f.label == "Password confirmation":
            f.label = "Parolni tasdiqlash"
    context = {
        'form': form
    }
    if request.method == "POST":
        form = UsersCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)

            messages.success(request, _("Foydalanuvchi ro`yhatdan o`tdi"))
            return redirect('users_list')
        else:
            messages.error(request, _("Foydalanuvchi ro`yxatdan o`tmadi"))
    return render(request, "adminpage/registretions_users.html", context)



def login_user(request):
    # if request.user.is_authenticated:
    #     return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                messages.success(request, _("Tizimga xush kelibsiz!"))
                return redirect("users_list")
            else:
                if request.user.is_blocked == False:
                    messages.success(request, _("Tizimga xush kelibsiz!"))
                    return redirect("statistics", pk=request.user.id )
                else:
                    messages.error(request, _('Siz admin tomonidan blocklangansiz!'))
                    return redirect("login")
        else:
            messages.error(request, _('Bundan login va parol mavjud emas!'))

    return render(request, "adminpage/login.html")



def user_account_edit(request, pk):
    user = get_object_or_404(UsersModel, id=pk)
    if request.method == 'POST':
        form = UsersChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,_('Tahrirlash bajarildi'))
            return redirect('admin_userpage', pk)
        else:
            messages.error(request,_("Xatolok yuz berdi"))
            return redirect('admin_userpage',pk)
    else:
        form = UsersChangeForm(instance=user)
        context = {
            'form':form,
        }
    return render(request,'adminpage/account_edit.html', context)



def user_account_delete(request,pk):
    user = get_object_or_404(UsersModel, id=pk)
    user.delete()
    return redirect('users_list')




@user_passes_test(lambda u: u.is_superuser)
def admin_change_user_password(request, user_id):
    user = get_object_or_404(UsersModel, id=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,_("Parol o`zgartirildi"))
            return redirect('admin_userpage', user_id)
        else:
            messages.error(request,_("Iltimos boshqa parol kiriting"))
            return redirect('error_url')
    else:
        form = SetPasswordForm(user)
        return render(request, 'adminpage/admin_change_user_password.html', {'form': form, 'user': user})

def admin_message(request):
    form = AdminMessageForm
    today = datetime.now()
    context = {
        'form':form,
    }
    if request.method == "POST":
        form = AdminMessageForm(request.POST)
        if form.is_valid():
            message_count = AdminMessageModel.objects.count()
            if message_count >= 5:
                five_days_ago = today - timedelta(days=5)
                oldest_message = AdminMessageModel.objects.filter(message_date__lte=five_days_ago).order_by('message_date').first()
                if oldest_message:
                    oldest_message.delete()
            form.save()
            messages.success(request, _("Xabar yuborildi"))
            return redirect('users_list')
        else:
            messages.error(request, _("Xabar yuborilmadi"))
    return render(request,'adminpage/admin_message.html', context)


def delete_message(request, pk):
    mes = get_object_or_404(AdminMessageModel, id=pk)
    mes.delete()
    messages.success(request, _("Xabar o`chirildi!"))
    return redirect("users_list")