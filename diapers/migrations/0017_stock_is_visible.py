# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0016_auto_20150918_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='is_visible',
            field=models.BooleanField(default=True),
        ),
    ]
