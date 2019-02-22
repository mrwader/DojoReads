# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-21 18:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_app', '0004_auto_20190221_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_reviews', to='dojo_app.Book'),
        ),
    ]
