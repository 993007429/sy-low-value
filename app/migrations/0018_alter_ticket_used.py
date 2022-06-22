# Generated by Django 4.0.3 on 2022-04-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_ticket_valid_ticket_expired_at_ticket_used'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='used',
            field=models.BooleanField(default=False, help_text='只能用一次，用过无效', verbose_name='是否用过'),
        ),
    ]
