# Generated by Django 4.0.5 on 2022-07-15 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recycle', '0027_platformmanager_region_platformmanager_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('serial', models.CharField(max_length=64, verbose_name='国标编号')),
                ('code', models.CharField(max_length=64, verbose_name='视频通道编号')),
                ('site_type', models.CharField(max_length=32, verbose_name='位置类型')),
                ('site_name', models.CharField(max_length=32, verbose_name='位置名称')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recycle.transferstation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
