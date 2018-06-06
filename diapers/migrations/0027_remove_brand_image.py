# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0026_auto_20180606_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='image',
        ),
    ]
