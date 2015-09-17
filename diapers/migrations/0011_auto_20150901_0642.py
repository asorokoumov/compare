# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0010_stock_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='max_weight',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_weight',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price_full',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price_unit',
            field=models.FloatField(),
        ),
    ]
