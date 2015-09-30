# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0015_auto_20150915_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]
