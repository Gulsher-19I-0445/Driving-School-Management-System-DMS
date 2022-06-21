# Generated by Django 4.0.3 on 2022-05-26 15:09

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_attendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=200, null=True, validators=[accounts.models.validate_edu_email_address]),
        ),
    ]