# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0017_stock_is_visible'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='price_unit_is_min',
        ),
    ]
