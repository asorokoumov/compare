# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0022_auto_20160517_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='series',
            field=models.ForeignKey(default=None, to='diapers.Series'),
        ),
    ]
