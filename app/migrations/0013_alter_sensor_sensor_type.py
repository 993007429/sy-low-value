# Generated by Django 4.0.3 on 2022-03-30 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_toiletcomment_toilet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='sensor_type',
            field=models.CharField(choices=[('PASSENGER_VOLUME', '客流检测仪'), ('H2S', '硫化氢监测仪'), ('NH3', '氨气监测仪'), ('MANAGEMENT_TERMINAL', '公厕智能管理终端'), ('TOILET_SEAT', '坑位状态监测仪'), ('AIR_QUALITY', '空气质量监测仪'), ('AMMETER', '电表'), ('WATER_METER', '水表'), ('BLUETOOTH_REPEATER', '蓝牙中继器'), ('OTHERS', '其他')], max_length=32, verbose_name='传感器类型'),
        ),
    ]
