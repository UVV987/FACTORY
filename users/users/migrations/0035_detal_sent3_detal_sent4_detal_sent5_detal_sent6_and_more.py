# Generated by Django 4.0.1 on 2022-02-14 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_remove_factory_end_start3_remove_factory_end_start4_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detal',
            name='sent3',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
        migrations.AddField(
            model_name='detal',
            name='sent4',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
        migrations.AddField(
            model_name='detal',
            name='sent5',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
        migrations.AddField(
            model_name='detal',
            name='sent6',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
        migrations.AddField(
            model_name='detal',
            name='sent7',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
        migrations.AddField(
            model_name='factory',
            name='sent1',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
        migrations.AddField(
            model_name='factory',
            name='sent2',
            field=models.BooleanField(default=False, verbose_name='отправлено'),
        ),
    ]