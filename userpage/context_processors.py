from .models import Unit,ProductModel,Product
from adminpage.models import AdminMessageModel
from datetime import datetime, timedelta

def units(request):
    units_list = Unit.objects.all()
    return {'units':units_list}

def products(request):
    products_list = Product.objects.all()
    return {'products':products_list}

def admin_messages(request):
    today = datetime.now()
    messages_list = AdminMessageModel.objects.all().order_by('-id')
    message_count = AdminMessageModel.objects.all().order_by('-id').count()
    if message_count >= 5:
        five_days_ago = today - timedelta(days=5)
        oldest_message = AdminMessageModel.objects.filter(message_date__lte=five_days_ago).order_by('message_date').first()
        if oldest_message:
            oldest_message.delete()
        message_delete = AdminMessageModel.objects.all().order_by('id').first()
        message_delete.delete()
    return {'admin_messages':messages_list}