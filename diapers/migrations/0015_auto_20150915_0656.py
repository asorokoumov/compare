# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0014_auto_20150915_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='price_full_before_discount',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price_unit_before_discount',
            field=models.FloatField(default=-1),
        ),
    ]
