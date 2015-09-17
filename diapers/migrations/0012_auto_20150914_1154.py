# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0011_auto_20150901_0642'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='price_full_before_discount',
            field=models.FloatField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stock',
            name='price_unit_before_discount',
            field=models.FloatField(default=-1),
            preserve_default=False,
        ),
    ]
