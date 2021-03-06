# Generated by Django 3.2.8 on 2021-12-27 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factory',
            name='contract_number',
        ),
        migrations.AddField(
            model_name='factory',
            name='contract',
            field=models.IntegerField(default=0, verbose_name='номер договора'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ContractUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.IntegerField(verbose_name='номер договора')),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.factory', verbose_name='factory, которому принадлежит контракт')),
            ],
        ),
    ]
