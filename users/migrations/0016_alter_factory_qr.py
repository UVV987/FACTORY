# Generated by Django 3.2.8 on 2022-01-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_factory_qr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factory',
            name='qr',
            field=models.ImageField(upload_to=''),
        ),
    ]
