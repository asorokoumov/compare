# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0006_auto_20150822_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='max_weight',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_weight',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price_full',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price_unit',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
