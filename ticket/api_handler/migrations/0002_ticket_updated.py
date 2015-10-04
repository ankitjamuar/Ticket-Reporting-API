# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('api_handler', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime.now, blank=True),
        ),
    ]
