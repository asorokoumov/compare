# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0013_stock_price_unit_is_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='price_unit_is_min',
            field=models.BooleanField(default=False),
        ),
    ]
