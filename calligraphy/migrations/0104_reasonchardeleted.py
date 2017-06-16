# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-16 12:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calligraphy', '0103_character_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReasonCharDeleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason_deleted', models.CharField(max_length=64)),
                ('target_char', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calligraphy.Character')),
                ('user_deleted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
