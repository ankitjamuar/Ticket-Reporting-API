# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_handler', '0002_ticket_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('updated', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('FK_account', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('FK_ticket', models.ForeignKey(to='api_handler.Ticket')),
            ],
        ),
    ]
