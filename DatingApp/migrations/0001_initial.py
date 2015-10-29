# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('uid', models.CharField(max_length=36, db_column='UId')),
                ('name', models.CharField(max_length=100, null=True, db_column='Name')),
                ('username', models.EmailField(unique=True, max_length=128, db_column='Email')),
                ('dob', models.DateTimeField(blank=True, null=True, db_column='DOB')),
                ('address', models.CharField(max_length=500, blank=True, null=True, db_column='Address')),
                ('isValidUser', models.IntegerField(default=0, db_column='isValidUser')),
                ('gender', models.IntegerField(default=0, db_column='Gender')),
                ('created', models.DateTimeField(auto_now=True, db_column='Created')),
                ('lastupdated', models.DateTimeField(auto_now=True, db_column='LastUpdated')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
