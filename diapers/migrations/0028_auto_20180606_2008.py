# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0027_remove_brand_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='description',
            field=models.TextField(default=None, null=True, blank=True),
        ),
    ]
