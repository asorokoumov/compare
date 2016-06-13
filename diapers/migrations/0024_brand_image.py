# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diapers', '0023_auto_20160530_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.TextField(default='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg', max_length=200),
            preserve_default=False,
        ),
    ]
