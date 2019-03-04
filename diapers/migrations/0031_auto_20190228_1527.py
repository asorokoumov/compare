# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0030_seller_name_rus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpreview',
            name='brand',
            field=models.ForeignKey(default=None, blank=True, to='diapers.Brand', null=True),
        ),
    ]
