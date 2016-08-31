# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-22 18:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160815_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-published_date', '-updated_date']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='timestamp',
            new_name='published_date',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='updated',
            new_name='updated_date',
        ),
    ]
