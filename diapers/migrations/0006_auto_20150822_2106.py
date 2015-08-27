# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0005_auto_20150822_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stock',
            old_name='price',
            new_name='price_full',
        ),
        migrations.AddField(
            model_name='stock',
            name='price_unit',
            field=models.FloatField(default=100),
            preserve_default=False,
        ),
    ]
