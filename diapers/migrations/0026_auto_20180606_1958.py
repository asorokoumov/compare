# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0025_skip'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='url_name',
            field=models.CharField(default='-2', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='url_name',
            field=models.CharField(default='-2', max_length=200),
            preserve_default=False,
        ),
    ]
