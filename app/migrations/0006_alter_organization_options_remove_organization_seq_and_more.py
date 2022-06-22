# Generated by Django 4.0.3 on 2022-03-14 05:13

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_toilettype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['pk']},
        ),
        migrations.RemoveField(
            model_name='organization',
            name='seq',
        ),
        migrations.CreateModel(
            name='Toilet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('code', models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='编号')),
                ('flush_type', models.CharField(blank=True, choices=[('BUBBLE', '发泡'), ('WATER', '冲水'), ('DRY', '旱厕'), ('WATER_VAPOR', '水汽一体'), ('OTHER', '其他')], max_length=32, null=True, verbose_name='冲洗方式')),
                ('road', models.CharField(blank=True, max_length=128, null=True, verbose_name='路段名称')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='占地面积')),
                ('built_at', models.DateTimeField(blank=True, null=True, verbose_name='建造时间')),
                ('men_toilet_nums', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='男厕位')),
                ('women_toilet_nums', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='女厕位')),
                ('genderless_toilet_nums', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='无性别厕位')),
                ('position_type', models.CharField(blank=True, choices=[('FIXED', '固定'), ('MOVABLE', '移动')], max_length=32, null=True, verbose_name='')),
                ('status', models.CharField(blank=True, choices=[('NORMAL', '正常'), ('OUT_OF_SERVICE', '停用'), ('MAINTAIN', '维修')], max_length=32, null=True, verbose_name='当前状态')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('remark', models.CharField(blank=True, max_length=255, null=True)),
                ('photos', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('supporting_facilities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('PAPER', '厕纸'), ('HAND_SANITIZER', '洗手液'), ('NURSING_ROOM', '母婴室'), ('GENDERLESS_ROOM', '第三性别卫生间'), ('WIFI', 'wifi'), ('AMMETER', '电表'), ('WATER_METER', '水表'), ('H2S', '硫化氢'), ('OUT_OF_SERVICE', '停用'), ('PAY', '收费')], max_length=32), size=None)),
                ('terminal_id', models.CharField(max_length=64, unique=True, verbose_name='终端号')),
                ('management', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.organization')),
                ('toilet_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.toilettype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('code', models.CharField(max_length=32, unique=True, verbose_name='传感器编号')),
                ('sensor_type', models.CharField(choices=[('PASSENGER_VOLUME', '客流检测仪'), ('H2S', '硫化氢监测仪'), ('NH3', '氨气监测仪'), ('MANAGEMENT_TERMINAL', '公厕智能管理终端'), ('TOILET_SEAT', '坑位状态监测仪'), ('AIR_QUALITY', '空气质量监测仪'), ('AMMETER', '电表'), ('WATER_METER', '水表'), ('OTHERS', '其他')], max_length=32, verbose_name='传感器类型')),
                ('installation_location', models.CharField(choices=[('MEM', '男厕'), ('WOMEN', '女厕'), ('GENDERLESS', '无差别卫生间'), ('ENTRY', '门口'), ('OTHERS', '其他')], max_length=32, verbose_name='安装位置')),
                ('serial', models.PositiveSmallIntegerField(blank=True, help_text='只有传感器类型是坑位传感器时才有效', null=True, verbose_name='厕位序号')),
                ('toilet', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='app.toilet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
