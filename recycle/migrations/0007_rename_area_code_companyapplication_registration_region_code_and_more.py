# Generated by Django 4.0.5 on 2022-06-27 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0006_remove_company_area_code_remove_company_area_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companyapplication',
            old_name='area_code',
            new_name='registration_region_code',
        ),
        migrations.RenameField(
            model_name='companyapplication',
            old_name='area_name',
            new_name='registration_region_name',
        ),
    ]
