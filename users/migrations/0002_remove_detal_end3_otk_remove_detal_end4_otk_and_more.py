# Generated by Django 4.0.1 on 2022-02-22 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detal',
            name='end3_otk',
        ),
        migrations.RemoveField(
            model_name='detal',
            name='end4_otk',
        ),
        migrations.RemoveField(
            model_name='detal',
            name='end5_otk',
        ),
        migrations.RemoveField(
            model_name='detal',
            name='end6_otk',
        ),
        migrations.RemoveField(
            model_name='detal',
            name='end7_otk',
        ),
        migrations.RemoveField(
            model_name='factory',
            name='end1_otk',
        ),
        migrations.RemoveField(
            model_name='factory',
            name='end2_otk',
        ),
    ]
