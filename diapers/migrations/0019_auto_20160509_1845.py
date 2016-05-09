# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0018_remove_stock_price_unit_is_min'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpreview',
            name='series',
            field=models.ForeignKey(default=None, blank=True, to='diapers.Series', null=True),
        ),
    ]
