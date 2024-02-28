from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from adminpage.models import UsersModel
from .forms import (
    ClientForm,
    ProductForm,
    ClientChangeForm,
    PasswordChangeingForm,
    AddUnitForm,
    AddProductForm,
    ProductChangeForm,
    # DateFilterForm
)
from adminpage.models import AdminMessageModel
from django.contrib import messages
from .models import ClientModel, ProductModel, Unit,Product
from django.contrib.auth.views import PasswordChangeView
# from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Sum,F, Func
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count
from datetime import datetime, timedelta

# import datetime 
from django.utils import timezone
# Create your views here.

@login_required(login_url='login')
def statistics_view(request, pk):
    users = UsersModel.objects.filter(id=pk)
    user = UsersModel.objects.get(id=pk)
    product = ProductModel.objects.filter(user_id=pk)
    count = Product.objects.filter(user_id = pk).count()
    client_count = ClientModel.objects.filter(user__id=pk).count()
    client_list = ClientModel.objects.filter(user_id=pk)
    message_text = AdminMessageModel.objects.order_by('-id').first()

    # products = Product.objects.filter(user_id = pk).values('product').annotate(product_count = Count('product'))
    today = datetime.now()
    to_month = datetime.now().month
    one_year = datetime.now().year
    to_sum_debt = 0
    to_sum_pay = 0
    monthly_debts = []
    product_sales = {}
    products = Product.objects.filter(user_id = pk)
    for p in products:
        sales = ProductModel.objects.filter(date__year = one_year,product_name = p).aggregate(total_sold=Sum('quantity_product'))
        if sales['total_sold']:
            product_sales[p.product] = sales['total_sold']


    class CastDate(Func):
        function = 'DATE'

    for month in range(1,13):
        total_debt = ProductModel.objects.annotate(date_as_datetime=CastDate(F('date'))).filter(date_as_datetime__year=one_year,date_as_datetime__month=month,user_id=pk).aggregate(Sum('debt'))
        monthly_debts.append(total_debt['debt__sum'] or 0)

    for x in product:
        if to_month == x.date.month:
            to_sum_debt += x.debt
            to_sum_pay += x.price*x.quantity_product
    
    if to_sum_pay: 
        b = (to_sum_debt*100)/to_sum_pay
    else:
        b = 0

    context = {
        'user':user,
        "users": users,
        'to_month':to_month,
        'to_sum_debt':to_sum_debt,
        'to_sum_pay':to_sum_pay,
        'b':b,
        'one_year':one_year,
        'monthly_debts':monthly_debts,
        'client_count':client_count,
        'client_list':client_list,
        'count':count,
        'product_sales':product_sales,
        'message_text':message_text,
        'today':today,



    }
    return render(request, "userpage/statistics.html", context)

def message_page(request,pk):
    message_p = AdminMessageModel.objects.order_by('-id').get(id=pk)
    context = {
        'message_p':message_p,
    }
    return render(request,'userpage/message_page.html',context)


@login_required(login_url='login')
def homepage_view(request, pk):
    if 'search' in request.GET:
        search = request.GET['search']
        list_clint = ClientModel.objects.filter(
            user__id=pk,
            name__icontains=search
        )
    else:
        list_clint = ClientModel.objects.filter(user__id=pk).order_by("-date")
    paginator = Paginator(list_clint, 10)

    page = request.GET.get("page")
    list_clint = paginator.get_page(page)
    
    user = UsersModel.objects.get(id=pk)
    
    context = {
        "user": user,
        "list_clint": list_clint,
    }
    return render(request, "userpage/userpages.html", context)

@login_required(login_url='login')
def client_add(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.user = UsersModel.objects.get(id=request.user.id)
            new_client.save()
            messages.success(request, _("Ro`yxatga yangi klient qo`shildi"))
            return redirect("userpages", pk=request.user.id)
        else:
            messages.error(request, _("Ro`yxatga yangi klient qo`shilmadi"))
    form = ClientForm()
    context = {
        "form": form,
    }

    return render(request, "userpage/add_client.html", context)


@login_required(login_url='login')
def add_unit(request):
    if request.method == "POST":
        form = AddUnitForm(request.POST)
        if form.data.get("unit_name") != "":
            unit_name = form.data.get(
            "unit_name"
            )  # unit_name o'zgaruvchisini oling, form nomiga qarab o'zgartiring
            if  unit_name:
                try:
                    existing_unit = Unit.objects.filter(Q(user_id = request.user.id) | Q(user__isnull =True)).get(unit_name=unit_name)
                    messages.error(request, _("Ushbu birlik avvalroq qo`shilgan"))
                    return redirect("add_unit")
                except Unit.DoesNotExist:
                    pass
            if form.is_valid():
                unit = form.save(commit=False)
                unit.unit_name = unit.unit_name.lower()
                unit.user = UsersModel.objects.get(id=request.user.id)
                unit.save()
                messages.success(request, _("Yangi birlik yaratildi!"))
                return redirect("userpages", pk=request.user.id)
            else:
                messages.error(request, _("Xatolok yuz berdi"))
                return redirect("userpages", pk=request.user.id)
        else:
            messages.error(request, _("Birlik nomi kiritilmadi"))
    form = AddUnitForm()
    context = {
        "form": form,
    }
    return render(request, "userpage/add_unit.html", context)


@login_required(login_url='login')
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.data.get('product') != "":
            product = form.data.get("product")
            if product:
                try:
                    existing_product = Product.objects.get(product=product)
                    messages.error(request,_("Ushbu mahsulot ro`yxatda mavjud"))
                    return redirect('add_product')
                except Product.DoesNotExist:
                    pass
            if form.is_valid():
                product = form.save(commit=False)
                product.product = product.product.lower()
                product.user = UsersModel.objects.get(id=request.user.id)
                product.save()
                messages.success(request,_("Mahsulot ro`yxatga qo`shildi"))
                return redirect('userpages',pk=request.user.id)
            else:
                messages.error(request, _("Xatolok yuz berdi"))
                return redirect("userpages", pk=request.user.id)
        else:
            messages.error(request, _("Birlik nomi kiritilmadi"))
            return redirect('add_product')
    form = AddProductForm()
    context = {
        'form':form,
    }

    return render(request, "userpage/add_product.html",context)




@login_required(login_url='login')
def client_edit(request, pk):
    client = get_object_or_404(ClientModel, id=pk)
    if request.method == "POST":
        form = ClientChangeForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, _("Tahrirlash bajarildi"))
            return redirect("userpages", pk=request.user.id)
        else:
            messages.error(request, _("Xatolok yuz berdi"))
            return redirect("userpages", pk=request.user.id)
    else:
        form = ClientChangeForm(instance=client)
        context = {
            "form": form,
        }
    return render(request, "userpage/client_edit.html", context)

@login_required(login_url='login')
def client_delete(request, pk):
    client = get_object_or_404(ClientModel, id=pk)
    client.delete()
    return redirect("userpages", pk=request.user.id)


@login_required(login_url='login')
def clientpage(request, pk):
    client = ClientModel.objects.get(id=pk)
    total_debt = 0

   

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)

    trade_list = ProductModel.objects.filter(date__range=(start_date, end_date),client_id=pk).order_by('-date')
    trade_lists = ProductModel.objects.filter(client_id=pk)
    for d in trade_lists:
        total_debt += d.debt

    context = {
        "client": client,
        "trade_list": trade_list,
        "total_debt": total_debt,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, "userpage/clientpage.html", context)

@login_required(login_url='login')
def to_sell_page(request, pk):
    client = ClientModel.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.user, request.POST)
        if form.is_valid():
            product_client = form.save(commit=False)
            product_client.client = ClientModel.objects.get(id=pk)
            product_client.user = UsersModel.objects.get(id=request.user.id)
            product_client.sum_price = float(
                product_client.price * product_client.quantity_product
            )
            if product_client.to_pay:
                if float(
                    product_client.price * product_client.quantity_product
                ) < float(product_client.to_pay):
                    messages.error(request, _("To`lov summasi noto`g`ri kiritildi"))
                    return redirect("to_sell_page", pk)
                else:
                    product_client.debt = float(
                        (product_client.price * product_client.quantity_product)
                        - (product_client.to_pay)
                    )
            else:
                product_client.debt = float(
                    product_client.price * product_client.quantity_product
                )
            product_client.save()
            messages.success(request, _("Clientga mahsulot qo`shildi"))
            return redirect("clientpage", pk)
        else:
            messages.error(request, _("Clientga mahsulot qo`shilmadi"))
    form = ProductForm(request.user)
    context = {
        "form": form,
        "client": client,
    }
    return render(request, "userpage/to_sell_page.html", context)

@login_required(login_url='login')
def payment_view(request, pk):
    client = ClientModel.objects.get(id=pk)
    trade_list = ProductModel.objects.filter(client=client, debt__gt=0)

    total_debt = sum([trade.debt for trade in trade_list])

    context = {
        "client": client,
        "trade_list": trade_list,
        "total_debt": total_debt,
    }
    return render(request, "userpage/payment.html", context)

@login_required(login_url='login')
def peyment_amount(request, pk):
    if request.method == "POST":
        payment_amount = float(request.POST["payment_amount"])
        client = ClientModel.objects.get(id=pk)
        trade_list = ProductModel.objects.filter(client=client, debt__gt=0)

        total_debt = sum([trade.debt for trade in trade_list])

        if payment_amount > total_debt:
            messages.info(request, _("Iltimos! To`lov miqdorini qayta tekshiring"))
            return redirect("clientpage", pk)
        else:
            for tarde in trade_list:
                if payment_amount >= tarde.debt:
                    payment_amount -= tarde.debt
                    tarde.debt = 0
                else:
                    tarde.debt -= payment_amount
                    payment_amount = 0

                tarde.save()

                if payment_amount == 0:
                    break
            return redirect("clientpage", pk)
    else:
        messages.error(request, _("Noto`g`ri so`rov yuborildi"))
        return redirect("clientpage", pk)

@login_required(login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(ProductModel, id=pk)
    product.delete()
    messages.success(request, _("Mahsulot o`chirildi!"))
    return redirect("clientpage", pk=product.client.id)


@login_required(login_url='login')
def unit_delete(request, pk):
    product = get_object_or_404(Unit, id=pk)
    product.delete()
    messages.success(request, _("Birlik o`chirildi!"))
    return redirect("statistics", pk=request.user.id)

@login_required(login_url='login')
def products_delete(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, _("Mahsulot o`chirildi!"))
    return redirect("statistics", pk=request.user.id)




@login_required(login_url='login')
def product_edit(request, pk):
    product = get_object_or_404(ProductModel, id=pk)
    if request.method == "POST":
        form = ProductChangeForm(request.user, request.POST, instance=product)
        if form.is_valid():
            product_client = form.save(commit=False)
            product_client.client.name = ProductModel.objects.get(id=pk)
            product_client.sum_price = float(
                product_client.price * product_client.quantity_product
            )
            if product_client.to_pay:
                if float(
                    product_client.price * product_client.quantity_product
                ) < float(product_client.to_pay):
                    messages.error(request, _("To`lov summasi noto`g`ri kiritildi"))
                    return redirect("product_edit", pk)
                else:
                    product_client.debt = float(
                        (product_client.price * product_client.quantity_product)
                        - (product_client.to_pay)
                    )
            else:
                product_client.debt = float(
                    product_client.price * product_client.quantity_product
                )
            product_client.save()
            messages.success(request, _("Mahsulot tahrirlandi"))
            return redirect("clientpage", pk=product.client.id)
        else:
            messages.error(request, _("Xatolik yuz berdi"))
            return redirect("clientpage", pk=product.client.id)
    form = ProductChangeForm(request.user, instance=product)
    context = {
        "form": form,
    }
    return render(request, "userpage/product_edit.html", context)


class PasswordChangeView(PasswordChangeView):
    from_class = PasswordChangeingForm
    success_url = reverse_lazy("success_password")

@login_required(login_url='login')
def password_success(request):
    return render(request, "userpage/success_password.html")
