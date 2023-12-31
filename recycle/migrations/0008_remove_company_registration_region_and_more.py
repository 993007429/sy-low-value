# Generated by Django 4.0.5 on 2022-06-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0007_rename_area_code_companyapplication_registration_region_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='registration_region',
        ),
        migrations.AddField(
            model_name='company',
            name='registration_region_code',
            field=models.CharField(default=1, max_length=32, verbose_name='注册区编码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='registration_region_name',
            field=models.CharField(default=1, max_length=32, verbose_name='注册区名称'),
            preserve_default=False,
        ),
    ]
