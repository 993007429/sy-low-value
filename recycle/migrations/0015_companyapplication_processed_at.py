# Generated by Django 4.0.5 on 2022-07-01 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0014_regionscope'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyapplication',
            name='processed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核时间'),
        ),
    ]