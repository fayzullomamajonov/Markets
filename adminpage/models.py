from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.

def validate_tell_num(tell):
    if( "+998" or tell.range == 9) in tell:
        return tell
    else:
        raise ValidationError("Telefon raqami +998 bilan boshlanishi kerak")


class UsersModel(AbstractUser):
    address = models.CharField(max_length=255)
    tell = models.CharField( blank=True,null=True,max_length=13,default='+998', validators=[validate_tell_num])
    date = models.DateField(null=True, blank=True, auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table= "UsersModel"

class AdminMessageModel(models.Model):
    message_title = models.CharField(max_length=25)
    message_description = models.TextField()
    message_date = models.DateField(null=True, blank=True,auto_now_add=True)

    def __str__(self) -> str:
        return self.message_title
    class Meta:
        db_table= "AdminMessageModel"