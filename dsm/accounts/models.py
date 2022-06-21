from django.db import models
import uuid


# Create your models here.
from django.forms import forms


def validate_edu_email_address(value):
    if not value.endswith('@gmail.com'):
        raise forms.ValidationError('Invalid email')

class Teacher(models.Model):
    #teacher_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(max_length=11, null=True)
    password_en = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    studentName = models.ForeignKey('customer', on_delete=models.CASCADE, related_name='teachers', blank=True,null=True)
    status=models.CharField(max_length=200, default='teacher')

    def __str__(self):
        return self.name


class customer(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    #customer_uuid = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, db_index=True)

    myteacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students' ,null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True,validators=[validate_edu_email_address])
    phone = models.IntegerField(max_length=11, null=True)
    password_en = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    isRegistered = models.BooleanField(default=False)
    plan=models.CharField(max_length=6,null=True)
    status = models.CharField(max_length=200, default='student')
    def __str__(self):
        return self.name


class attendance(models.Model):

    studentName=models.ForeignKey('customer',on_delete=models.CASCADE,related_name='attendance',null=False)
    date=models.DateField(default='2022-05-23')
    status=models.CharField(max_length=200,default="Present")
    score=models.FloatField(default=0.0)




