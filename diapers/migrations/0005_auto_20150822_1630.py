# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0004_auto_20150822_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='manufacturer',
            new_name='brand',
        ),
        migrations.RenameField(
            model_name='series',
            old_name='manufacturer',
            new_name='brand',
        ),
    ]
