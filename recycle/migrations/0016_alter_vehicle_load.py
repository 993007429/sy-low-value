# Generated by Django 4.0.5 on 2022-07-01 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0015_companyapplication_processed_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='load',
            field=models.FloatField(verbose_name='载重（t）'),
        ),
    ]
