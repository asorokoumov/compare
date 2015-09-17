# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0009_previewparsehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='in_stock',
            field=models.CharField(default='Yes', max_length=200),
            preserve_default=False,
        ),
    ]
