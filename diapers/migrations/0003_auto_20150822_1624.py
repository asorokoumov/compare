# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0002_auto_20150822_1449'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Manufacturer',
            new_name='Brand',
        ),
    ]
