# Generated by Django 4.0.6 on 2022-12-09 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0037_highvaluereport'),
    ]

    operations = [
        migrations.CreateModel(
            name='HazardousWasteCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=128, verbose_name='密码')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='highvaluereport',
            name='high_value_weight',
            field=models.FloatField(verbose_name='高值重量（单位kg）'),
        ),
        migrations.AlterField(
            model_name='highvaluereport',
            name='low_value_weight',
            field=models.FloatField(verbose_name='低值重量（单位kg）'),
        ),
        migrations.CreateModel(
            name='HazardousWasteReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('report_date', models.DateField(verbose_name='填报日期')),
                ('weight', models.FloatField(verbose_name='高值重量（单位kg）')),
                ('approver', models.CharField(max_length=64, verbose_name='审核人')),
                ('company', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='recycle.hazardouswastecompany')),
            ],
            options={
                'unique_together': {('company', 'report_date')},
            },
        ),
    ]
