# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
                ('file', models.FileField(null=True, upload_to=b'./root')),
            ],
        ),
    ]