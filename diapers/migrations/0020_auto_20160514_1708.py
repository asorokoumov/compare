# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0019_auto_20160509_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='description',
            field=models.TextField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='description',
            field=models.TextField(default=None, null=True, blank=True),
        ),
    ]
