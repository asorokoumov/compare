# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0012_auto_20150914_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='price_unit_is_min',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
