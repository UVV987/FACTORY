# Generated by Django 4.0.1 on 2022-02-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_detal_end3_otk_remove_detal_end4_otk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detal',
            name='end3_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
        migrations.AddField(
            model_name='detal',
            name='end4_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
        migrations.AddField(
            model_name='detal',
            name='end5_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
        migrations.AddField(
            model_name='detal',
            name='end6_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
        migrations.AddField(
            model_name='detal',
            name='end7_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
        migrations.AddField(
            model_name='factory',
            name='end1_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
        migrations.AddField(
            model_name='factory',
            name='end2_otk',
            field=models.BooleanField(default=False, verbose_name='ОТК закончен'),
        ),
    ]
