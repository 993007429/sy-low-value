# Generated by Django 4.0.6 on 2022-07-19 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0028_monitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclehistory',
            name='plate_number',
            field=models.CharField(max_length=32, verbose_name='车牌号'),
        ),
    ]
