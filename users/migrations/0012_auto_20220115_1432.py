# Generated by Django 3.2.8 on 2022-01-15 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20220110_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='detal',
            name='contract',
            field=models.TextField(default=0, verbose_name='номер договора'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detal',
            name='order_number',
            field=models.IntegerField(default=0, verbose_name='номер заказа'),
            preserve_default=False,
        ),
    ]
