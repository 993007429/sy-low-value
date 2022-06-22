# Generated by Django 4.0.3 on 2022-03-16 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_toilet_built_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='installation_location',
            field=models.CharField(choices=[('MEN', '男厕'), ('WOMEN', '女厕'), ('GENDERLESS', '无差别卫生间'), ('ENTRY', '门口'), ('OTHERS', '其他')], max_length=32, verbose_name='安装位置'),
        ),
        migrations.CreateModel(
            name='ToiletComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('ratings', models.SmallIntegerField(choices=[(3, 'Satisfied'), (2, 'Acceptable'), (1, 'Dissatisfied')], verbose_name='评价星级')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='评论内容')),
                ('toilet', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='app.toilet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
