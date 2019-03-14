# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0031_auto_20190228_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='series',
            field=models.ForeignKey(default=None, blank=True, to='diapers.Series', null=True),
        ),
    ]
