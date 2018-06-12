# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0028_auto_20180606_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='gender',
            name='gender_rus',
            field=models.CharField(default='-1', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='type',
            name='type_rus',
            field=models.CharField(default='-1', max_length=200),
            preserve_default=False,
        ),
    ]
