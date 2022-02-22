# Generated by Django 4.0 on 2021-12-27 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='чертеж')),
                ('order_number', models.IntegerField(verbose_name='номер заказа')),
                ('start_data', models.DateField(verbose_name='дата начало')),
                ('end_start', models.DateField(verbose_name='дата окончания')),
                ('weight', models.FloatField(verbose_name='масса')),
                ('contract_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.factory', verbose_name='номер договора')),
            ],
        ),
    ]
