# Generated by Django 4.0.6 on 2022-08-02 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0031_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_licence',
            field=models.CharField(max_length=2084, null=True, verbose_name='行驶证'),
        ),
        migrations.AddField(
            model_name='vehicleapplication',
            name='vehicle_licence',
            field=models.CharField(max_length=2084, null=True, verbose_name='行驶证'),
        ),
        migrations.AddField(
            model_name='vehicledraft',
            name='vehicle_licence',
            field=models.CharField(max_length=2084, null=True, verbose_name='行驶证'),
        ),
        migrations.AddField(
            model_name='vehiclehistory',
            name='vehicle_licence',
            field=models.CharField(max_length=2084, null=True, verbose_name='行驶证'),
        ),
    ]