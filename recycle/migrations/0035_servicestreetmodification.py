# Generated by Django 4.0.6 on 2022-11-10 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0034_alter_event_options_alter_inboundrecord_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceStreetModification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('plate_number', models.CharField(max_length=32, verbose_name='车牌号')),
                ('read', models.BooleanField(default=False, verbose_name='已读')),
                ('source_street', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='source_service_street_modifications', to='recycle.region')),
                ('target_street', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='target_service_street_modifications', to='recycle.region')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]